from fastapi import WebSocket
from typing import Optional
import json
import asyncio
import random
import string
from .engine import create_deck, sort_tiles, check_pung, check_kong, check_hu

class Player:
    def __init__(self, pid: int, ws: WebSocket, nickname: str):
        self.pid = pid
        self.ws = ws
        self.nickname = nickname
        self.hand = []
        self.melds = []
        self.discards = []
        self.ready = False
        self.score = 0
        self.pending_actions = []

    async def send(self, data: dict):
        try:
            await self.ws.send_text(json.dumps(data, ensure_ascii=False))
        except Exception:
            pass

    def hand_json(self, hide=False):
        if hide:
            return {"hand_len": len(self.hand), "melds": self.melds, "discards": len(self.discards)}
        return {
            "hand": sort_tiles(self.hand),
            "melds": self.melds,
            "discards": len(self.discards),
        }

    @property
    def hand_count(self):
        return len(self.hand)


class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.players: list[Optional[Player]] = [None] * 4
        self.status = "waiting"
        self.deck = []
        self.wall_count = 0
        self.current_turn = 0
        self.last_discard = None
        self.last_discard_player = None
        self.last_discard_owner = None
        self.pending_action_players = set()
        self.pending_action_timer = None
        self.waiting_for_actions = False
        self.dealer = 0
        self.action_events = {}
        self.current_turn_backup = None

    @property
    def player_count(self):
        return sum(1 for p in self.players if p is not None)

    @property
    def available_seat(self):
        for i, p in enumerate(self.players):
            if p is None:
                return i
        return None

    async def broadcast(self, data: dict, exclude: Optional[int] = None):
        for p in self.players:
            if p and p.pid != exclude:
                await p.send(data)

    async def send_to(self, pid: int, data: dict):
        p = self.players[pid]
        if p:
            await p.send(data)

    async def start_game(self):
        self.status = "playing"
        self.deck = create_deck()
        self.wall_count = len(self.deck)

        for p in self.players:
            if p:
                p.hand = [self.deck.pop() for _ in range(13)]
                p.melds = []
                p.discards = []
                p.score = 0

        self.wall_count = len(self.deck)

        for i, p in enumerate(self.players):
            if p:
                p_public = []
                for j, op in enumerate(self.players):
                    if op:
                        p_public.append({"pid": j, "nickname": op.nickname, "hand_len": 13, "melds": []})
                await p.send({
                    "type": "game_start",
                    "your_seat": i,
                    "dealer": self.dealer,
                    "players": p_public,
                    "hand": sort_tiles(p.hand),
                    "wall_count": self.wall_count,
                })

        self.current_turn = self.dealer
        await self._draw_tile(self.current_turn)

    async def _draw_tile(self, pid: int):
        if not self.deck:
            await self.broadcast({"type": "draw_standoff", "message": "流局"})
            self.status = "waiting"
            return

        tile = self.deck.pop()
        self.wall_count = len(self.deck)
        p = self.players[pid]

        p.hand.append(tile)

        if check_hu(p.hand):
            await self.send_to(pid, {"type": "self_hu_prompt", "tile": tile, "wall_count": self.wall_count})
            return

        await self.send_to(pid, {
            "type": "draw",
            "tile": tile,
            "hand": sort_tiles(p.hand),
            "wall_count": self.wall_count,
        })
        await self.broadcast({
            "type": "player_drew",
            "pid": pid,
            "wall_count": self.wall_count,
        }, exclude=pid)
        await self.send_to(pid, {"type": "your_turn", "wall_count": self.wall_count})

    async def handle_discard(self, pid: int, tile: str):
        if self.waiting_for_actions:
            await self.send_to(pid, {"type": "error", "message": "等待其他玩家操作"})
            return

        p = self.players[pid]
        if tile not in p.hand:
            await self.send_to(pid, {"type": "error", "message": "手中没有这张牌"})
            return

        p.hand.remove(tile)
        p.discards.append(tile)
        self.last_discard = tile
        self.last_discard_owner = pid

        await self.broadcast({
            "type": "discard",
            "pid": pid,
            "tile": tile,
            "discard_count": len(p.discards),
            "hand": sort_tiles(p.hand) if pid == self.current_turn else {"hand_len": len(p.hand)},
            "wall_count": self.wall_count,
        })

        responders = []
        for i, other in enumerate(self.players):
            if other and i != pid:
                actions = []
                has_pung = check_pung(other.hand, tile)
                has_kong = check_kong(other.hand, tile)
                test_hand = other.hand + [tile]
                has_hu = check_hu(sort_tiles(test_hand))

                if has_hu:
                    actions.append("hu")
                if has_pung:
                    actions.append("pung")
                if has_kong:
                    actions.append("kong")
                if actions:
                    responders.append((i, actions))

        if responders:
            self.waiting_for_actions = True
            for i, actions in responders:
                self.players[i].pending_actions = actions
                await self.send_to(i, {
                    "type": "action_prompt",
                    "actions": actions,
                    "tile": tile,
                    "from_pid": pid,
                })

            self.current_turn_backup = pid
            self.pending_action_players = {i for i, _ in responders}
            self.pending_action_timer = asyncio.create_task(self._action_timeout())

        else:
            await self._next_turn(pid)

    async def _action_timeout(self):
        await asyncio.sleep(8)
        for pid in list(self.pending_action_players):
            self.pending_action_players.discard(pid)
            await self.send_to(pid, {"type": "action_result", "action": "pass"})
        await self._finalize_action()

    async def handle_action(self, pid: int, action: str):
        if not self.waiting_for_actions:
            await self.send_to(pid, {"type": "error", "message": "没有可用的操作"})
            return

        if pid not in self.pending_action_players:
            await self.send_to(pid, {"type": "error", "message": "你不在等待操作列表中"})
            return

        if self.pending_action_timer:
            self.pending_action_timer.cancel()
            self.pending_action_timer = None

        if action == "pass":
            self.pending_action_players.discard(pid)
            await self.send_to(pid, {"type": "action_result", "action": "pass"})
            if not self.pending_action_players:
                await self._finalize_action()
            else:
                self.pending_action_timer = asyncio.create_task(self._action_timeout())
            return

        if action == "hu":
            winner = self.players[pid]
            winner.hand.append(self.last_discard)
            await self.broadcast({
                "type": "game_over",
                "winner": pid,
                "winner_nickname": winner.nickname,
                "hand": sort_tiles(winner.hand),
                "win_tile": self.last_discard,
                "action": "hu",
            })
            self.status = "waiting"
            return

        if action == "pung":
            p = self.players[pid]
            p.hand.remove(self.last_discard)
            p.hand.remove(self.last_discard)
            p.melds.append(("pung", self.last_discard, self.last_discard_owner))

            self.current_turn = pid
            self.waiting_for_actions = False
            self.pending_action_players.clear()

            await self.broadcast({
                "type": "action_taken",
                "pid": pid,
                "action": "pung",
                "tile": self.last_discard,
                "from_pid": self.last_discard_owner,
            })
            await self._draw_tile(pid)
            return

        if action == "kong":
            p = self.players[pid]
            p.hand.remove(self.last_discard)
            p.hand.remove(self.last_discard)
            p.hand.remove(self.last_discard)
            p.melds.append(("kong", self.last_discard, self.last_discard_owner))

            self.current_turn = pid
            self.waiting_for_actions = False
            self.pending_action_players.clear()

            await self.broadcast({
                "type": "action_taken",
                "pid": pid,
                "action": "kong",
                "tile": self.last_discard,
                "from_pid": self.last_discard_owner,
            })
            await self._draw_tile(pid)
            return

    async def _finalize_action(self):
        self.waiting_for_actions = False
        self.pending_action_players.clear()
        await self._next_turn(self.last_discard_owner)

    async def _next_turn(self, from_pid: int):
        self.current_turn = (from_pid + 1) % 4
        await self._draw_tile(self.current_turn)

    def remove_player(self, pid: int):
        self.players[pid] = None
        if self.player_count == 0:
            return
        self.status = "waiting"


rooms: dict[str, Room] = {}

def generate_room_id():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

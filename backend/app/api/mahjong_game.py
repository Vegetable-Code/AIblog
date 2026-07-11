from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..game.room_manager import Room, Player, rooms, generate_room_id
import json

router = APIRouter()

@router.websocket("/ws/game/{room_id}")
async def game_websocket(websocket: WebSocket, room_id: str):
    await websocket.accept()
    nickname = None
    player = None
    room = rooms.get(room_id)

    try:
        data = await websocket.receive_text()
        msg = json.loads(data)
        if msg.get("type") != "join":
            await websocket.send_text(json.dumps({"type": "error", "message": "First message must be join"}))
            return

        nickname = msg.get("nickname", "Anonymous")

        if room is None:
            await websocket.send_text(json.dumps({"type": "error", "message": "Room not found"}))
            return

        seat = room.available_seat
        if seat is None:
            await websocket.send_text(json.dumps({"type": "error", "message": "Room is full"}))
            return

        player = Player(seat, websocket, nickname)
        room.players[seat] = player

        await player.send({"type": "joined", "pid": seat, "room_id": room_id, "seat": seat, "players_in_room": room.player_count})
        await room.broadcast({"type": "player_joined", "pid": seat, "nickname": nickname, "players_in_room": room.player_count}, exclude=seat)

        # Send existing players to the new joiner
        existing_players = []
        for i, p in enumerate(room.players):
            if p and i != seat:
                existing_players.append({"pid": i, "nickname": p.nickname, "ready": p.ready})
        if existing_players:
            await player.send({"type": "existing_players", "players": existing_players})

        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)
            msg_type = msg.get("type")

            if msg_type == "ready":
                player.ready = True
                await room.broadcast({"type": "player_ready", "pid": player.pid})
                ready_count = sum(1 for p in room.players if p and p.ready)
                if room.player_count >= 2 and ready_count == room.player_count:
                    await room.start_game()

            elif msg_type == "discard":
                tile = msg.get("tile")
                if player.pid == room.current_turn:
                    await room.handle_discard(player.pid, tile)
                else:
                    await player.send({"type": "error", "message": "不是你的回合"})

            elif msg_type == "action":
                action = msg.get("action")
                await room.handle_action(player.pid, action)

            elif msg_type == "ping":
                await player.send({"type": "pong"})

    except (WebSocketDisconnect, Exception):
        pass
    finally:
        if room and player:
            seat = player.pid
            room.remove_player(seat)
            await room.broadcast({"type": "player_left", "pid": seat, "nickname": nickname})
        try:
            await websocket.close()
        except Exception:
            pass

@router.post("/game/room/create")
async def create_room():
    room_id = generate_room_id()
    rooms[room_id] = Room(room_id)
    return {"room_id": room_id}

@router.get("/game/room/{room_id}")
async def get_room(room_id: str):
    room = rooms.get(room_id)
    if not room:
        return {"exists": False}
    return {"exists": True, "room_id": room.room_id, "player_count": room.player_count, "status": room.status}

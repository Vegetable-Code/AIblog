from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..game.room_manager import Room, Player, rooms, generate_room_id
from ..core.database import SessionLocal
from ..models.user import User
from ..core.config import settings
from jose import jwt, JWTError
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

        # Validate JWT token to get user
        token = msg.get("token", "")
        username = None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
        except Exception:
            await websocket.send_text(json.dumps({"type": "error", "message": "Invalid token"}))
            return
        if not username:
            await websocket.send_text(json.dumps({"type": "error", "message": "Invalid token"}))
            return
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
        finally:
            db.close()
        if not user:
            await websocket.send_text(json.dumps({"type": "error", "message": "User not found"}))
            return
        nickname = user.nickname or user.username

        if room is None:
            await websocket.send_text(json.dumps({"type": "error", "message": "Room not found"}))
            return

        seat = room.available_seat
        if seat is None:
            await websocket.send_text(json.dumps({"type": "error", "message": "Room is full"}))
            return

        player = Player(seat, websocket, nickname)
        room.players[seat] = player

        all_players = []
        for i, p in enumerate(room.players):
            if p:
                all_players.append({"pid": i, "nickname": p.nickname, "hand_len": len(p.hand), "melds": p.melds, "ready": p.ready})

        await player.send({"type": "joined", "pid": seat, "room_id": room_id, "seat": seat, "players": all_players})
        await room.broadcast({"type": "player_joined", "pid": seat, "nickname": nickname, "players_in_room": room.player_count}, exclude=seat)

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

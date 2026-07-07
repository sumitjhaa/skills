"""WebSockets: connection management, broadcast, chat room, event handling."""
from typing import Any, Optional
from datetime import datetime
import json
import time
import threading
import random


# ======================== WebSocket Simulation ========================

class WebSocketConnection:
    """Simulates a single WebSocket connection."""
    def __init__(self, conn_id: str, room: str = "general"):
        self.conn_id = conn_id
        self.room = room
        self.connected = True
        self.messages: list[dict] = []
        self.joined_at = datetime.now()

    def send_json(self, data: dict):
        if not self.connected:
            raise RuntimeError("Connection closed")
        self.messages.append(data)

    def close(self):
        self.connected = False

    def receive(self) -> dict:
        """Simulate receiving a message."""
        return {"type": "ping"}


class WebSocketManager:
    """Manages all WebSocket connections and rooms."""
    def __init__(self):
        self.connections: dict[str, WebSocketConnection] = {}
        self.rooms: dict[str, list[str]] = {}
        self._next_id = 0

    def connect(self, room: str = "general") -> WebSocketConnection:
        self._next_id += 1
        conn_id = f"conn_{self._next_id}"
        conn = WebSocketConnection(conn_id, room)
        self.connections[conn_id] = conn

        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(conn_id)

        # Broadcast join event
        self.broadcast(room, {"type": "user_joined", "conn_id": conn_id, "room": room}, exclude=conn_id)
        return conn

    def disconnect(self, conn_id: str):
        conn = self.connections.get(conn_id)
        if conn is None:
            return
        room = conn.room
        conn.close()

        # Remove from room
        if room in self.rooms and conn_id in self.rooms[room]:
            self.rooms[room].remove(conn_id)

        # Broadcast leave event
        self.broadcast(room, {"type": "user_left", "conn_id": conn_id, "room": room})
        del self.connections[conn_id]

    def broadcast(self, room: str, message: dict, exclude: str | None = None):
        """Send message to all connections in a room."""
        if room not in self.rooms:
            return
        for conn_id in self.rooms[room]:
            if conn_id != exclude:
                conn = self.connections.get(conn_id)
                if conn and conn.connected:
                    conn.send_json(message)

    def send_to(self, conn_id: str, message: dict):
        """Send message to a specific connection."""
        conn = self.connections.get(conn_id)
        if conn and conn.connected:
            conn.send_json(message)

    def get_room_users(self, room: str) -> list[dict]:
        """Get all users in a room."""
        users = []
        for conn_id in self.rooms.get(room, []):
            conn = self.connections.get(conn_id)
            if conn:
                users.append({"conn_id": conn.conn_id, "room": conn.room, "joined_at": conn.joined_at.isoformat()})
        return users

    def room_count(self, room: str) -> int:
        return len(self.rooms.get(room, []))

    def stats(self) -> dict:
        return {
            "total_connections": len(self.connections),
            "total_rooms": len(self.rooms),
            "rooms": {room: len(conns) for room, conns in self.rooms.items()},
        }


# ======================== Chat Room Simulation ========================

class ChatRoom:
    """Simulates a real-time chat room."""
    def __init__(self, ws_manager: WebSocketManager):
        self.ws = ws_manager
        self.message_history: dict[str, list[dict]] = {}

    def handle_message(self, conn_id: str, data: dict):
        """Process an incoming chat message."""
        msg_type = data.get("type", "message")
        room = data.get("room", "general")
        username = data.get("username", "anonymous")
        content = data.get("content", "")

        if msg_type == "join":
            # Move connection to room
            conn = self.ws.connections.get(conn_id)
            if conn:
                old_room = conn.room
                if old_room in self.ws.rooms and conn_id in self.ws.rooms[old_room]:
                    self.ws.rooms[old_room].remove(conn_id)
                conn.room = room
                if room not in self.ws.rooms:
                    self.ws.rooms[room] = []
                self.ws.rooms[room].append(conn_id)
            return {"type": "system", "content": f"{username} joined {room}"}

        elif msg_type == "message":
            msg = {
                "type": "chat_message",
                "username": username,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "room": room,
            }
            if room not in self.message_history:
                self.message_history[room] = []
            self.message_history[room].append(msg)
            self.ws.broadcast(room, msg)
            return msg

        elif msg_type == "typing":
            self.ws.broadcast(room, {"type": "typing", "username": username, "room": room}, exclude=conn_id)
            return {"type": "typing_ack"}

        return {"type": "error", "content": f"Unknown message type: {msg_type}"}


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.ws = WebSocketManager()
        self.chat = ChatRoom(self.ws)

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def post(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return deco

    def delete(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "DELETE", "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== Endpoints ========================

@app.post("/ws/connect")
def ws_connect(room: str = "general"):
    """Simulate a WebSocket connection."""
    conn = app.ws.connect(room)
    return {"conn_id": conn.conn_id, "room": conn.room, "status": "connected"}


@app.post("/ws/{conn_id}/disconnect")
def ws_disconnect(conn_id: str):
    """Simulate closing a WebSocket connection."""
    conn = app.ws.connections.get(conn_id)
    if conn is None:
        return {"error": "Connection not found"}
    app.ws.disconnect(conn_id)
    return {"conn_id": conn_id, "status": "disconnected"}


@app.post("/ws/{conn_id}/message")
def ws_send_message(conn_id: str, type: str = "message", room: str = "general", username: str = "anonymous", content: str = ""):
    """Send a message via WebSocket."""
    conn = app.ws.connections.get(conn_id)
    if conn is None:
        return {"error": "Connection not found"}
    data = {"type": type, "room": room, "username": username, "content": content}
    result = app.chat.handle_message(conn_id, data)
    return {"conn_id": conn_id, "result": result}


@app.get("/ws/rooms")
def list_rooms():
    """List all active rooms with user counts."""
    rooms = {}
    for room, conns in app.ws.rooms.items():
        rooms[room] = {"users": len(conns), "connections": conns}
    return {"rooms": rooms, "total_rooms": len(rooms)}


@app.get("/ws/rooms/{room}/users")
def room_users(room: str):
    """List users in a specific room."""
    users = app.ws.get_room_users(room)
    return {"room": room, "users": users, "count": len(users)}


@app.get("/ws/rooms/{room}/history")
def room_history(room: str, limit: int = 20):
    """Get message history for a room."""
    history = app.chat.message_history.get(room, [])
    return {"room": room, "messages": history[-limit:], "total": len(history)}


@app.get("/ws/stats")
def ws_stats():
    """WebSocket server stats."""
    return app.ws.stats()


# ======================== Demo ========================
print("=== WebSockets Demo ===\n")

# Simulate multiple users connecting
print("1. Users connecting to rooms:")
alice = app("POST", "/ws/connect", room="general")
print(f"   Alice connected: {alice['data']['conn_id']}")

bob = app("POST", "/ws/connect", room="general")
print(f"   Bob connected: {bob['data']['conn_id']}")

charlie = app("POST", "/ws/connect", room="random")
print(f"   Charlie connected: {charlie['data']['conn_id']} (different room)\n")

# Send messages
print("2. Alice sends a message:")
msg1 = app("POST", f"/ws/{alice['data']['conn_id']}/message",
    type="message", room="general", username="Alice", content="Hello everyone!")
print(f"   {json.dumps(msg1['data']['result'], indent=2)}\n")

print("3. Bob replies:")
msg2 = app("POST", f"/ws/{bob['data']['conn_id']}/message",
    type="message", room="general", username="Bob", content="Hi Alice!")
print(f"   {json.dumps(msg2['data']['result'], indent=2)}\n")

print("4. More messages:")
for i, msg in enumerate(["How are you?", "I'm great!", "Anyone want to code?"]):
    app("POST", f"/ws/{alice['data']['conn_id']}/message",
        type="message", room="general", username="Alice", content=msg)

# Check room state
print("5. Room listing:")
rooms = app("GET", "/ws/rooms")
print(f"   {json.dumps(rooms['data'], indent=2)}\n")

print("6. Users in general:")
users = app("GET", "/ws/rooms/general/users")
print(f"   {json.dumps(users['data'], indent=2)}\n")

print("7. Message history for general:")
history = app("GET", "/ws/rooms/general/history", limit=5)
print(f"   {json.dumps(history['data'], indent=2)}\n")

# Disconnect
print("8. Bob disconnects:")
disc = app("POST", f"/ws/{bob['data']['conn_id']}/disconnect")
print(f"   {disc['data']}\n")

print("9. Room after disconnect:")
rooms2 = app("GET", "/ws/rooms")
print(f"   {json.dumps(rooms2['data'], indent=2)}\n")

print("10. Server stats:")
stats = app("GET", "/ws/stats")
print(f"   {json.dumps(stats['data'], indent=2)}")

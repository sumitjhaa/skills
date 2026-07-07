# 🔌 WebSockets
<!-- ⏱️ 15 min | 🟢 Supplement -->

**What You'll Learn:** WebSocket connections, broadcast, rooms, real-time chat.

## Install

```bash
pip install websockets
```

## Basic WebSocket

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

## Connection Manager

```python
class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: str):
        for ws in self.active:
            await ws.send_text(message)
```

## Chat Rooms

```python
class RoomManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(room, []).append(ws)
        await self.broadcast(room, f"User joined")

    async def broadcast(self, room: str, message: str):
        for ws in self.rooms.get(room, []):
            await ws.send_text(message)
```

## Event Types

| Event | Direction | Purpose |
|-------|-----------|---------|
| `connect` | Client → Server | Open connection |
| `disconnect` | Client → Server | Close connection |
| `message` | Bidirectional | Chat/data |
| `ping/pong` | Bidirectional | Keep alive |

## Run the Code

```bash
python code/22-websockets.py
```

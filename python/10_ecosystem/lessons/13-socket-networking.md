# 🔌 Socket Networking & Selectors I/O
<!-- ⏱️ 20 min read | 🔴 Mastery | 🧠 Applied -->

**What You'll Learn:** TCP/UDP sockets (`socket`), non-blocking I/O, and the `selectors` module for event-driven networking — the foundation beneath every web framework.

> 💡 **TL;DR — The whole point:** `socket` is the lowest-level network API in Python. `selectors` lets you efficiently watch many sockets at once (like a mini event loop). Every web framework (FastAPI, Django, Flask) is built on these primitives.

## 🔗 Why This Matters
When you need raw control (game servers, custom protocols, port scanners), understanding socket programming is essential. `selectors` is how async frameworks handle thousands of connections without threads.

## The Concept

| Component | Job |
|-----------|-----|
| `socket()` | create an endpoint (AF_INET + SOCK_STREAM for TCP) |
| `bind()` + `listen()` + `accept()` | server setup |
| `connect()` | client connection |
| `send()` / `recv()` | data transfer |
| `setblocking(False)` | non-blocking mode |
| `selectors.DefaultSelector` | efficient I/O multiplexing |

**TCP vs UDP:** TCP = reliable, ordered, stream-oriented. UDP = unreliable, unordered, datagram-oriented (gaming, DNS, streaming).

## Code Example

```python
"""TCP echo server + client with selectors for non-blocking I/O."""
import socket
import selectors
import sys

HOST, PORT = "127.0.0.1", 9999
sel = selectors.DefaultSelector()


def accept(sock: socket.socket) -> None:
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, data=b"")
    print(f"Accepted: {addr}")


def read(conn: socket.socket, data: bytes) -> None:
    recv_data = conn.recv(1024)
    if recv_data:
        conn.sendall(recv_data)  # echo
        data += recv_data
    else:
        sel.unregister(conn)
        conn.close()


def run_server() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, data=None)

    for _ in range(4):  # handle 4 events then exit
        events = sel.select(timeout=1)
        for key, _ in events:
            if key.data is None:
                accept(key.fileobj)
            else:
                read(key.fileobj, key.data)
    sel.close()


if __name__ == "__main__":
    run_server()
    print("Echo server demo complete")
```

## 🔍 How It Works
- `socket.socket(AF_INET, SOCK_STREAM)` — creates a TCP socket
- `sock.bind((host, port))` — binds to an address; `sock.listen(5)` starts listening with backlog
- `sock.accept()` — blocks until a client connects; returns `(conn, addr)`
- `sock.connect((host, port))` — client connects
- `sock.send(data)` / `sock.recv(bufsize)` — send/receive bytes
- `sock.setblocking(False)` — operations return immediately; would-block raises `BlockingIOError`
- `selectors.DefaultSelector.register(sock, EVENT_READ, data=x)` — watch for readable events
- `selector.select(timeout)` — blocks until events fire; returns `(key, events)` tuples
- `EVENT_READ` = socket has data to read; `EVENT_WRITE` = socket ready to accept writes

**UDP:** `socket(AF_INET, SOCK_DGRAM)`, no `listen()`/`accept()`, use `sendto()`/`recvfrom()`.

## ⚠️ Common Pitfall
**Blocking calls block everything.** In a single-threaded server, `recv()` blocks the entire process. Always use `setblocking(False)` + `selectors`, or use threads/asyncio for each connection.

**Partial sends:** `send()` may not send all bytes. Always check return value or use `sendall()`. Similarly, `recv(1024)` may return fewer bytes than the message.

## 🧠 Memory Aid
"Socket = phone. bind/listen/accept = get a number, turn on ringer, pick up. connect = dial. send/recv = talk/listen. setblocking(False) = 'don't wait on hold.' Selector = receptionist who tells you which line has a caller."

## 🏃 Try It
Write a simple HTTP client that connects to `httpbin.org:80`, sends a GET /get request, and prints the response headers and body. Use `selectors` with a 5s timeout.

## 🔗 Related
- [Asyncio Primitives Deep](12-asyncio-primitives-deep.md) — higher-level async networking
- [Signal & ContextVars](14-signal-contextvars.md) — OS integration
- [Deployment & Monitoring](09-deployment-monitoring.md) — production networking

## ➡️ Next
[Signal, ContextVars & OS Integration](14-signal-contextvars.md)

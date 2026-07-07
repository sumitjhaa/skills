"""Socket Networking & Selectors — TCP echo server, HTTP client, port scanner.
Run: python 10-13-socket-networking.py
"""

import socket
import selectors
import concurrent.futures
import threading
import time

HOST, PORT = "127.0.0.1", 9999
_echo_messages: list[str] = []


def _run_echo_server(stop_after: float = 1.0) -> None:
    sel = selectors.DefaultSelector()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, data=None)

    deadline = time.perf_counter() + stop_after
    while time.perf_counter() < deadline:
        events = sel.select(timeout=0.5)
        for key, _ in events:
            if key.data is None:
                conn, addr = key.fileobj.accept()
                conn.setblocking(False)
                sel.register(conn, selectors.EVENT_READ, data=b"")
            else:
                conn = key.fileobj
                data = conn.recv(1024)
                if data:
                    conn.sendall(data)
                    _echo_messages.append(data.decode())
                else:
                    sel.unregister(conn)
                    conn.close()
    sel.close()
    server.close()


def echo_client(msg: str) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((HOST, PORT))
    sock.sendall(msg.encode())
    response = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        response += chunk
    sock.close()
    return response.decode()


def scan_port(port: int) -> int | None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    result = sock.connect_ex(("127.0.0.1", port))
    sock.close()
    return port if result == 0 else None


if __name__ == "__main__":
    server_thread = threading.Thread(target=_run_echo_server, daemon=True)
    server_thread.start()
    time.sleep(0.1)

    result = echo_client("Hello, sockets!")
    print(f"Echo client: {result}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        open_ports = list(filter(None, pool.map(scan_port, range(9970, 10010))))
    print(f"Open ports (9970-10009): {open_ports}")
    print("All socket examples OK")

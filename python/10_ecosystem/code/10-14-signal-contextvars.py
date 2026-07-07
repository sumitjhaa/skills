"""Signal, AtExit, FaultHandler & ContextVars — OS & async context.
Run: python 10-14-signal-contextvars.py
"""

import signal
import atexit
import faulthandler
import contextvars
import time
import asyncio
from typing import Any

faulthandler.enable()

# ── Graceful shutdown flag ──
shutdown_requested = False


def handle_sigterm(signum: int, frame: Any) -> None:
    global shutdown_requested
    shutdown_requested = True


signal.signal(signal.SIGTERM, handle_sigterm)

# ── atexit cleanup ──
@atexit.register
def cleanup() -> None:
    pass  # pretend to close DB connections


# ── ContextVar for request tracing ──
request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")
user_id: contextvars.ContextVar[int] = contextvars.ContextVar("user_id", default=0)


async def handle_request(rid: str, uid: int) -> None:
    request_id.set(rid)
    user_id.set(uid)
    await asyncio.sleep(0.1)
    print(f"  Processing {request_id.get()} for user {user_id.get()}")


async def main() -> None:
    # ContextVar isolation across tasks
    async with asyncio.TaskGroup() as tg:
        tg.create_task(handle_request("req-1", 42))
        tg.create_task(handle_request("req-2", 99))
    print(f"  Default context: {request_id.get('not-set')}")

    # copy_context
    ctx = contextvars.copy_context()
    ctx.run(lambda: print(f"  Copy context: request_id={request_id.get('unset')}"))

    # SIGALRM timeout
    def timeout_handler(signum: int, frame: Any) -> None:
        raise TimeoutError("Operation timed out")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(1)
    try:
        time.sleep(5)
    except TimeoutError:
        print("  SIGALRM: timed out after 1s")
    signal.alarm(0)

    print("All signal/contextvars examples OK")


if __name__ == "__main__":
    asyncio.run(main())

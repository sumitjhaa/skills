"""GC & weakref: memory leak detection, observer pattern, auto-cleanup cache"""
import gc, weakref, sys

class EventBus:
    """Observer pattern: subscribers held as weak refs so they can be garbage collected"""
    def __init__(self):
        self._subscribers: list[weakref.ref] = []  # Weak refs — won't prevent GC

    def subscribe(self, callback):
        self._subscribers.append(weakref.ref(callback))  # No strong reference kept

    def emit(self, event: str):
        alive = []
        for ref in self._subscribers:
            cb = ref()  # Returns None if callback was garbage collected
            if cb is not None:
                cb(event)
                alive.append(ref)
        self._subscribers = alive  # Remove dead (collected) subscribers

def on_event(msg):
    """Callback — would be GC'd if bus didn't hold weak refs"""
    print(f"  Event: {msg}")

# --- Usage ---
bus = EventBus()
bus.subscribe(on_event)
bus.emit("user_login")  # Prints "Event: user_login"

# --- GC introspection (debugging memory leaks) ---
circular = {}  # Create circular reference
circular["self"] = circular  # obj points to itself — ref count never reaches 0
n = gc.collect()  # Force GC collection — returns number of collected objects
print(f"GC collected {n} unreachable objects")

# --- weakref.finalize: cleanup without __del__ (more reliable) ---
class DatabaseConnection:
    def close(self):
        print("  Connection closed")

db = DatabaseConnection()
weakref.finalize(db, db.close)  # Calls db.close() when db is garbage collected
del db  # Triggers finalize (more reliable than __del__)

"""Signals: built-in & custom signals, receivers, disconnecting."""
from typing import Any, Callable
from collections import defaultdict
from functools import wraps


# ======================== Signal/Dispatcher Simulation ========================

class Signal:
    """Simulates Django's django.dispatch.Signal."""
    def __init__(self, providing_args: list[str] = None):
        self.providing_args = providing_args or []
        self._receivers: list[Callable] = []

    def connect(self, receiver: Callable, sender: Any = None, weak: bool = True, dispatch_uid: str = None):
        """Register a receiver function."""
        self._receivers.append(receiver)

    def disconnect(self, receiver: Callable = None, dispatch_uid: str = None):
        """Remove a receiver."""
        if receiver:
            self._receivers = [r for r in self._receivers if r != receiver]

    def send(self, sender: Any = None, **kwargs):
        """Send signal to all connected receivers. Returns list of (receiver, response)."""
        results = []
        for receiver in self._receivers:
            try:
                result = receiver(sender=sender, signal=self, **kwargs)
                results.append((receiver, result))
            except Exception as e:
                results.append((receiver, e))
        return results

    def __call__(self, **kwargs):
        """Shortcut decorator: @signal.connect"""
        def decorator(fn):
            self.connect(fn)
            return fn
        return decorator


# ======================== Django Built-in Signal Proxies ========================

# In Django, these come from django.db.models.signals
pre_save = Signal(providing_args=["instance", "raw"])
post_save = Signal(providing_args=["instance", "created"])
pre_delete = Signal(providing_args=["instance"])
post_delete = Signal(providing_args=["instance"])
m2m_changed = Signal(providing_args=["action", "model", "pk_set"])


# ======================== Model Simulation ========================

MODEL_STORE: dict[str, list] = {
    "Post": [],
    "Comment": [],
    "AuditLog": [],
}

class Model:
    """Simulates a Django model with signal-emitting save/delete."""
    _model_name = "Base"

    def __init__(self, **kwargs):
        self.pk = len(MODEL_STORE.get(self._model_name, [])) + 1
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self, *args, **kwargs):
        pre_save.send(sender=self.__class__, instance=self)
        MODEL_STORE[self._model_name].append(self)
        post_save.send(sender=self.__class__, instance=self, created=True)

    def delete(self):
        pre_delete.send(sender=self.__class__, instance=self)
        MODEL_STORE[self._model_name] = [
            item for item in MODEL_STORE[self._model_name]
            if getattr(item, 'pk', None) != self.pk
        ]
        post_delete.send(sender=self.__class__, instance=self)


class Post(Model):
    _model_name = "Post"

class Comment(Model):
    _model_name = "Comment"


# ======================== Signal Handlers ========================

@post_save.connect
def update_post_count(sender, instance, created: bool, **kwargs):
    """Auto-update some counter when a post is saved."""
    if created and sender._model_name == "Post":
        print(f"  [SIGNAL] Post created: #{instance.pk} — updating post count")


@post_save.connect
def create_audit_log(sender, instance, created: bool, **kwargs):
    """Log every model save for audit."""
    entry = f"Audit: {sender._model_name} #{instance.pk} {'created' if created else 'updated'}"
    audit_entry = {"message": entry}
    MODEL_STORE["AuditLog"].append(audit_entry)
    print(f"  [SIGNAL] {entry}")


# Using decorator shortcut
@post_delete.connect
def cleanup_on_delete(sender, instance, **kwargs):
    print(f"  [SIGNAL] {sender._model_name} #{instance.pk} deleted — cleaning up")


# Custom signal
post_viewed = Signal(providing_args=["post", "user", "ip_address"])

@post_viewed.connect
def increment_view_count(sender, post, user, **kwargs):
    """Track page views."""
    print(f"  [CUSTOM] Post #{post.pk} viewed by {user}")

@post_viewed.connect
def record_view_history(sender, post, user, **kwargs):
    """Record view in history."""
    history = MODEL_STORE.setdefault("ViewHistory", [])
    history.append({"post_id": post.pk, "user": user})


# ======================== Demo ========================
print("=== Signals Demo ===\n")

# --- Pre/post save signals ---
print("1. Creating a Post (triggers post_save):")
post = Post(title="Hello Signals", content="Signal content")
post.save()

print("\n2. Creating another Post:")
post2 = Post(title="Second Post", content="More content")
post2.save()

# --- Delete signal ---
print(f"\n3. Deleting Post #1:")
post.delete()

# --- Custom signal ---
print("\n4. Custom signal (post_viewed):")
post_viewed.send(sender=Post, post=post2, user="alice", ip_address="127.0.0.1")

# --- Disconnect a receiver ---
print("\n5. Disconnecting update_post_count, then creating Post #3:")
post_save.disconnect(update_post_count)

post3 = Post(title="No Count Update", content="Test")
post3.save()
print("  (update_post_count signal handler was NOT called)")

# Reconnect for cleanup
post_save.connect(update_post_count)

# --- Show audit log ---
print(f"\n6. Audit log entries: {len(MODEL_STORE['AuditLog'])}")
for entry in MODEL_STORE["AuditLog"]:
    print(f"   - {entry['message']}")

"""Session management & security: session lifecycle, CSRF, security headers."""
from typing import Optional
import secrets
import hashlib
import time
from functools import wraps


# ======================== Session Store ========================
SESSION_STORE: dict[str, dict] = {}  # session_id → session_data


class Session:
    """Simulates Django's session object."""

    def __init__(self, session_id: str = None):
        self.session_id = session_id or secrets.token_hex(32)
        self.data = SESSION_STORE.get(self.session_id)
        if self.data is None:
            SESSION_STORE[self.session_id] = {}
            self.data = SESSION_STORE[self.session_id]
        self.created_at = self.data.get("_created_at", time.time())
        self.modified = False

    def __getitem__(self, key: str):
        return self.data[key]

    def __setitem__(self, key: str, value):
        self.data[key] = value
        SESSION_STORE[self.session_id] = self.data
        self.modified = True

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set_expiry(self, seconds: int):
        self.data["_expiry"] = time.time() + seconds
        self.modified = True

    def is_expired(self) -> bool:
        expiry = self.data.get("_expiry", float("inf"))
        return time.time() > expiry

    def save(self):
        self.data["_created_at"] = self.created_at
        SESSION_STORE[self.session_id] = self.data

    def flush(self):
        if self.session_id in SESSION_STORE:
            del SESSION_STORE[self.session_id]
        self.data = {}

    @property
    def session_key(self) -> str:
        return self.session_id


class SessionMiddleware:
    """Simulates Django's session middleware — attaches session to request."""

    def process_request(self, request: dict):
        cookie = request.get("cookies", {})
        session_id = cookie.get("sessionid")
        if session_id and session_id in SESSION_STORE:
            session = Session(session_id)
            if session.is_expired():
                session.flush()
                request["session"] = Session()
            else:
                request["session"] = session
        else:
            request["session"] = Session()
        request["session_id"] = request["session"].session_id
        # Track session ID so subsequent accesses use the same key
        request["cookies"] = {**request.get("cookies", {}),
                              "sessionid": request["session"].session_id}

    def process_response(self, request: dict, response: dict):
        session = request.get("session")
        if session and session.modified:
            session.save()
            response.setdefault("cookies", {})
            response["cookies"]["sessionid"] = {
                "value": session.session_id,
                "httponly": True,
                "secure": True,
                "samesite": "Lax",
            }
        return response


# ======================== CSRF Protection ========================

CSRF_TOKENS: dict[str, str] = {}  # session_id → csrf_token


def get_csrf_token(request: dict) -> str:
    """Get or generate CSRF token for the current session."""
    session_id = request.get("session_id", "")
    token = CSRF_TOKENS.get(session_id)
    if not token:
        token = secrets.token_hex(32)
        CSRF_TOKENS[session_id] = token
    return token


def csrf_protect(func):
    """Decorator: validate CSRF token on POST requests."""
    @wraps(func)
    def wrapper(request: dict, *args, **kwargs):
        if request.get("method", "GET") == "POST":
            csrf_cookie = request.get("cookies", {}).get("csrftoken", "")
            csrf_form = request.get("post", {}).get("csrfmiddlewaretoken", "")
            if not csrf_cookie or csrf_cookie != csrf_form:
                return {"status": 403, "error": "CSRF token missing or invalid"}
        return func(request, *args, **kwargs)
    return wrapper


@csrf_protect
def transfer_view(request: dict) -> dict:
    return {"status": 200, "message": "Transfer completed"}


# ======================== Security Headers ========================

class SecurityMiddleware:
    """Add security headers to every response."""

    HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Content-Security-Policy": "default-src 'self'",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    def process_response(self, request: dict, response: dict) -> dict:
        response.setdefault("headers", {}).update(self.HEADERS)
        return response


# ======================== Session Security Best Practices ========================

def regenerate_session_id(request: dict):
    """Regenerate session ID after login (session fixation prevention)."""
    old_session = request.get("session")
    if old_session:
        old_session.flush()
        # Copy data to new session
        old_data = dict(old_session.data)
    else:
        old_data = {}
    new_session = Session()
    for k, v in old_data.items():
        if not k.startswith("_"):
            new_session[k] = v
    request["session"] = new_session
    request["session_id"] = new_session.session_id
    return new_session


def enforce_https(func):
    """Decorator: reject non-HTTPS requests."""
    @wraps(func)
    def wrapper(request: dict, *args, **kwargs):
        if not request.get("is_secure", False):
            return {"status": 301, "location": f"https://{request.get('host', '')}{request.get('path', '')}"}
        return func(request, *args, **kwargs)
    return wrapper


@enforce_https
def secure_view(request: dict) -> dict:
    return {"status": 200, "message": "Secure content"}


# ======================== Demo ========================
print("=== Session & Security Demo ===")

# Session lifecycle
req: dict = {"cookies": {}, "method": "GET"}
SessionMiddleware().process_request(req)
session = req["session"]
session["username"] = "alice"
session["cart"] = ["item1", "item2"]
session.set_expiry(3600)
session.save()
print(f"Session created: {session.session_key[:16]}...")
print(f"  username: {session['username']}")
print(f"  cart: {session['cart']}")
print(f"  expiry: {session.get('_expiry') > time.time()} (not expired)")

# Session on next request (same cookie)
req2: dict = {"cookies": {"sessionid": session.session_key}, "method": "GET"}
SessionMiddleware().process_request(req2)
session2 = req2["session"]
print(f"\nSame session: {session2.session_key[:16]}...")
print(f"  username: {session2['username']}")

# CSRF protection
csrf_req: dict = {"method": "POST", "session_id": "test123", "cookies": {"csrftoken": "abc"},
                   "post": {"csrfmiddlewaretoken": "abc"}}
print(f"\nCSRF valid: {transfer_view(csrf_req)}")

csrf_bad: dict = {"method": "POST", "session_id": "test123", "cookies": {"csrftoken": "abc"},
                   "post": {"csrfmiddlewaretoken": "wrong"}}
print(f"CSRF invalid: {transfer_view(csrf_bad)}")

# HTTPS enforcement
secure_req: dict = {"is_secure": True}
print(f"\nSecure: {secure_view(secure_req)}")

insecure_req: dict = {"is_secure": False, "host": "example.com", "path": "/login/"}
print(f"Insecure: {secure_view(insecure_req)}")

# Session fixation prevention
session_reg = regenerate_session_id(req)
print(f"\nSession regenerated: {session_reg.session_key[:16]}...")
print(f"  Old session exists: {session.session_key in SESSION_STORE}")

# Security headers
sec_mw = SecurityMiddleware()
resp = sec_mw.process_response({}, {"status": 200})
print(f"\nSecurity headers: {resp.get('headers', {})}")

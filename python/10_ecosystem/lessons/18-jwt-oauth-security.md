# 🔐 JWT & OAuth Security
<!-- ⏱️ 16 min | 🔴 Advanced | 🧠 Production -->

**What You'll Learn:** Implement authentication and authorization using JWT tokens, OAuth2 flows, and password hashing with bcrypt — the security backbone of modern web APIs.

> 💡 **TL;DR — The whole point:** Hash passwords with bcrypt. Issue JWTs for stateless auth. Use OAuth2 for third-party login (Google, GitHub). Never store plaintext passwords, never roll your own crypto.

## 🔗 Why This Matters
Every production API needs authentication. JWT is the industry standard for stateless auth tokens. OAuth2 is how users log in with Google/GitHub. Together they form the security foundation of virtually every modern web application.

## The Concept

| Concept | What It Does |
|---------|-------------|
| **bcrypt** | Hash passwords (slow by design, salt built-in) |
| **JWT** | Stateless token with claims (who, when, permissions) |
| **Access Token** | Short-lived (15 min), sent with every request |
| **Refresh Token** | Long-lived (7 days), used to get new access tokens |
| **OAuth2** | Delegated auth — app asks provider "is this user real?" |
| **Bearer Token** | `Authorization: Bearer <token>` header |

## Code Example

```python
"""JWT auth + bcrypt password hashing + OAuth2 pattern."""
import hashlib
import json
import time
import hmac
from base64 import urlsafe_b64encode, urlsafe_b64decode
from dataclasses import dataclass

# ---- Minimal JWT implementation (for learning) ----
# In production, use: pip install pyjwt (PyJWT library)

SECRET = "super-secret-key-change-in-production"


def base64url_encode(data: bytes) -> str:
    return urlsafe_b64encode(data).rstrip(b"=").decode()


def base64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return urlsafe_b64decode(s)


def create_jwt(payload: dict, secret: str = SECRET, expires_in: int = 900) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {**payload, "iat": int(time.time()), "exp": int(time.time()) + expires_in}
    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())
    signing_input = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
    return f"{signing_input}.{base64url_encode(signature)}"


def verify_jwt(token: str, secret: str = SECRET) -> dict | None:
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
        signing_input = f"{header_b64}.{payload_b64}"
        expected_sig = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
        expected_b64 = base64url_encode(expected_sig)
        if sig_b64 != expected_b64:
            return None
        payload = json.loads(base64url_decode(payload_b64))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except (ValueError, json.JSONDecodeError, KeyError):
        return None


# ---- Password hashing (bcrypt-style) ----

def hash_password(password: str) -> str:
    """Simulate bcrypt hash (production: pip install bcrypt)."""
    salt = hashlib.sha256(password.encode()).hexdigest()[:22]
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"pbkdf2$sha256$100000${salt}${hashed.hex()}"


def verify_password(password: str, stored: str) -> bool:
    parts = stored.split("$")
    salt, expected_hash = parts[3], parts[4]
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return actual.hex() == expected_hash


# ---- Demo ----

print("=== JWT Tokens ===")
payload = {"sub": "user_42", "role": "admin", "name": "Alice"}
token = create_jwt(payload)
print(f"Token: {token[:80]}...")
decoded = verify_jwt(token)
print(f"Verified: {decoded['sub']} ({decoded['role']})")

tampered = token[:-5] + "AAAAA"
print(f"Tampered token verified: {verify_jwt(tampered)}")

print("\n=== Password Hashing ===")
pw_hash = hash_password("MyS3cret!")
print(f"Hash: {pw_hash[:50]}...")
print(f"Correct password: {verify_password('MyS3cret!', pw_hash)}")
print(f"Wrong password:   {verify_password('WrongPass', pw_hash)}")

print("\n=== OAuth2 Pattern (Authorization Code Flow) ===")
print("""
1. User clicks "Login with Google"
2. App redirects to: https://accounts.google.com/o/oauth2/auth?client_id=APP_ID&redirect_uri=CALLBACK&scope=email+profile
3. User approves → Google redirects to CALLBACK?code=AUTH_CODE
4. App sends AUTH_CODE + client_secret to Google's token endpoint
5. Google returns {"access_token": "...", "refresh_token": "...", "id_token": "..."}
6. App decodes id_token (JWT) → gets user's email + name
7. App creates its own JWT session token for the user
""")

print("\n=== Production checklist ===")
checks = [
    "Use bcrypt (not SHA) for password storage",
    "Use PyJWT library (not manual HMAC)",
    "Set short access token expiry (15 min)",
    "Use refresh tokens for longer sessions",
    "Store secrets in env vars / secrets manager",
    "Use HTTPS everywhere (never send tokens over HTTP)",
    "Validate all JWT claims (iss, aud, exp)",
    "Rate-limit login endpoints",
]
for i, check in enumerate(checks, 1):
    print(f"  {i}. {check}")
```

## 🔍 How It Works
- JWT has three parts: `header.payload.signature` — each base64url-encoded and dot-separated
- The signature is HMAC-SHA256 of `header.payload` using the server's secret key
- `verify_jwt` recomputes the signature and checks expiry — no database lookup needed (stateless)
- bcrypt is intentionally slow (~100ms per hash) to resist brute-force attacks
- OAuth2 Authorization Code Flow is the safest pattern — the client never sees the user's password
- `pkcs5` password hashing (PBKDF2) is the "poor man's bcrypt" — use actual bcrypt in production

## ⚠️ Common Pitfall
- Rolling your own crypto — always use well-audited libraries (PyJWT, bcrypt, python-jose)
- Not validating `aud` (audience) claim — any token from your auth provider could be used
- Storing tokens in `localStorage` (vulnerable to XSS) — use httpOnly cookies instead
- Not rotating the JWT secret — if it leaks, all tokens are compromised

## 🧠 Memory Aid
"Hash passwords with bcrypt (slow is safe). Issue JWTs with short expiry. Use OAuth2 for third-party login. Never trust the client."

## 🏃 Try It
Add a `@require_auth` decorator that extracts and verifies a JWT from the `Authorization: Bearer <token>` header. Apply it to the Flask API from lesson 17.

## 🔗 Related
- [Hashlib, Secrets & UUID](../05_modules_io/lessons/09-hashlib-secrets-uuid.md) — password hashing basics
- [Web Frameworks](17-flask-django.md) — securing Flask/Django apps
- [FastAPI Deep](06-fastapi-deep.md) — FastAPI's built-in OAuth2 support
- [Pydantic & Settings](../09_production/lessons/13-pydantic-settings.md) — managing SECRET_KEY via env vars

## ➡️ Next
[19 — Async MongoDB with Motor](19-motor-async-mongodb.md)

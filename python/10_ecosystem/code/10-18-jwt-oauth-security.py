"""JWT auth + bcrypt password hashing + OAuth2 pattern."""
import hashlib
import json
import time
import hmac
from base64 import urlsafe_b64encode, urlsafe_b64decode

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


def hash_password(password: str) -> str:
    salt = hashlib.sha256(password.encode()).hexdigest()[:22]
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"pbkdf2$sha256$100000${salt}${hashed.hex()}"


def verify_password(password: str, stored: str) -> bool:
    parts = stored.split("$")
    salt, expected_hash = parts[3], parts[4]
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return actual.hex() == expected_hash


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

print("\n=== Production checklist ===")
checks = [
    "Use bcrypt (not SHA) for password storage",
    "Use PyJWT library (not manual HMAC)",
    "Set short access token expiry (15 min)",
    "Use refresh tokens for longer sessions",
    "Store secrets in env vars / secrets manager",
    "Use HTTPS everywhere",
    "Validate all JWT claims (iss, aud, exp)",
    "Rate-limit login endpoints",
]
for i, check in enumerate(checks, 1):
    print(f"  {i}. {check}")

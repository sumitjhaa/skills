# 🔐 Hashlib, Secrets & UUID
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** How to hash passwords securely, generate cryptographically safe tokens, and create unique IDs with UUID.

> 💡 **TL;DR — The whole point:** `hashlib` for integrity, `secrets` for security, `uuid` for uniqueness — the three pillars of secure data handling.

## 🔗 Why This Matters
Useful modules showed you `hashlib` basics. Now go deeper: password hashing with PBKDF2, secure random tokens for API keys, and UUIDs for database primary keys.

## The Concept
Three modules for three distinct needs:
- **hashlib** — one-way hashing for passwords, file integrity checks
- **secrets** — cryptographically secure random (for tokens, reset links)
- **uuid** — globally unique identifiers (128-bit, no collisions)

`random` is for simulation/games. `secrets` is for security-critical randomness.

## Code Example

```python
"""Password hashing, secure tokens, and UUID generation."""

import hashlib
import secrets
import uuid


def hash_password_pbkdf2(password: str) -> tuple:
    """Hash a password with PBKDF2 (production-ready)."""
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return (salt, hashed.hex())


def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """Verify a password against its hash."""
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return hashed.hex() == stored_hash


def generate_api_key() -> str:
    """Generate a secure API key."""
    return f"sk-{secrets.token_hex(24)}"


def generate_uuid_id() -> str:
    """Generate a UUID4 (random) identifier."""
    return str(uuid.uuid4())


# Password hashing demo
salt, hashed = hash_password_pbkdf2("secure_pass_123")
print(f"Salt: {salt[:8]}... Hash: {hashed[:16]}...")
print(f"Verify correct: {verify_password('secure_pass_123', salt, hashed)}")
print(f"Verify wrong: {verify_password('wrong_pass', salt, hashed)}")

# API keys & UUIDs
print(f"API Key: {generate_api_key()}")
print(f"User ID: {generate_uuid_id()}")
```

## 🔍 How It Works
- `hashlib.pbkdf2_hmac` uses PBKDF2 with HMAC-SHA256 — slow by design (100K iterations)
- `secrets.token_hex(n)` returns n random bytes as hex string (cryptographically secure)
- `uuid.uuid4()` generates a random UUID with 122 bits of entropy
- `secrets` uses the OS's CSPRNG (`/dev/urandom` on Linux)

## ⚠️ Common Pitfall
Using `random` for security. `random` uses Mersenne Twister — predictable if you observe enough outputs. Always use `secrets` for tokens, passwords, and keys.

## 🧠 Memory Aid
**"hashlib = one-way, secrets = secure-random, uuid = unique-ID"**: Each serves one purpose: hash for integrity, secrets for security, UUID for identity.

## 🏃 Try It
Write a function `store_user(username, password)` that returns a dict with `username`, `salt`, `password_hash`, and `user_id` (UUID). Then write `authenticate(username, password, users_db)` that verifies credentials.

## 🔗 Related
- [Useful Modules →](./08-useful-modules.md)
- [Subprocess & Shutil →](./10-subprocess-shutil.md)

## ➡️ Next
[Subprocess & Shutil](./10-subprocess-shutil.md)

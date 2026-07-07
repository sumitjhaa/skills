"""Password hashing, secure tokens, and UUID generation."""
import hashlib
import secrets
import uuid


def hash_password_pbkdf2(password: str) -> tuple:
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return (salt, hashed.hex())


def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return hashed.hex() == stored_hash


def generate_api_key() -> str:
    return f"sk-{secrets.token_hex(24)}"


def generate_uuid_id() -> str:
    return str(uuid.uuid4())


def store_user(username: str, password: str) -> dict:
    salt, hashed = hash_password_pbkdf2(password)
    return {"username": username, "salt": salt, "password_hash": hashed, "user_id": generate_uuid_id()}


def authenticate(username: str, password: str, users_db: list) -> bool:
    for user in users_db:
        if user["username"] == username:
            return verify_password(password, user["salt"], user["password_hash"])
    return False


salt, hashed = hash_password_pbkdf2("secure_pass_123")
print(f"Verify: {verify_password('secure_pass_123', salt, hashed)}")
print(f"API Key: {generate_api_key()}")
print(f"UUID: {generate_uuid_id()}")

users_db = [store_user("alice", "pass1")]
print(f"Auth alice: {authenticate('alice', 'pass1', users_db)}")
print(f"Auth alice wrong: {authenticate('alice', 'wrong', users_db)}")

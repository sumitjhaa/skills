# 🔐 JWT Authentication
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** JSON Web Tokens, token creation/verification, expiration, protecting endpoints.

## Install

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

## Create a JWT

```python
from datetime import datetime, timedelta
from jose import jwt

SECRET = "your-secret-key"
ALGORITHM = "HS256"
EXPIRATION = 30  # minutes

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
```

<!-- 🧠 Never hardcode the secret. Use environment variables. -->

## Verify a JWT

```python
def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

## JWT Structure

```
header.payload.signature
```

| Part | Content |
|------|---------|
| header | `{"alg": "HS256", "typ": "JWT"}` |
| payload | `{"sub": 1, "exp": 1700000000}` |
| signature | HMAC-SHA256(header + payload, secret) |

## Protected Endpoint

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_me(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": payload["sub"]}
```

## Standard Claims

| Claim | Meaning |
|-------|---------|
| `sub` | Subject (user ID) |
| `exp` | Expiration timestamp |
| `iat` | Issued at |
| `role` | Custom — user's role |

## Run the Code

```bash
python code/14-jwt-auth.py
```

# 🔑 OAuth2 Password Flow
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Password hashing, `/token` endpoint, scopes, OAuth2 compliance.

## Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

<!-- 🔒 Never store plain text passwords. bcrypt includes a salt automatically. -->

## /token Endpoint

```python
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id, "scopes": form_data.scopes})
    return {"access_token": token, "token_type": "bearer"}
```

## Scopes

Scopes limit what a token can do:

```python
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    scopes = form_data.scopes.split() if form_data.scopes else ["read"]
    token = create_access_token({"sub": user.id, "scopes": scopes})
    return {"access_token": token, "token_type": "bearer", "scope": " ".join(scopes)}
```

| Scope | Permission |
|-------|------------|
| `read` | Read resources |
| `write` | Create/update resources |
| `admin` | Administrative actions |

## Dependency with Scopes

```python
from fastapi.security import SecurityScopes

def require_scope(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401)
    token_scopes = payload.get("scopes", [])
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail="Insufficient scope")
    return payload
```

## Run the Code

```bash
python code/15-oauth2-password-flow.py
```

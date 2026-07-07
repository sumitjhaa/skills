# 👤 Current User Dependency
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Extract current user from token, chain dependencies, reusable auth patterns.

## The Pattern

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.get_user(payload["sub"])
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

<!-- 🧩 `get_current_user` becomes reusable across every protected endpoint. -->

## Using It

```python
@app.get("/users/me")
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/users/me/items")
def read_my_items(current_user: User = Depends(get_current_user)):
    return get_items_for_user(current_user.id)
```

## Dependency Chain

```
get_authorization_header   ← extracts Bearer token from header
    ↓
get_token_payload          ← verifies JWT, returns payload
    ↓
get_current_user           ← looks up user in DB from payload["sub"]
    ↓
get_current_active_user    ← checks user.is_active
    ↓
✅ Protected endpoint
```

<!-- 🪜 Each layer adds a specific check. Test each dependency independently. -->

## Active User Guard

```python
def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

## Run the Code

```bash
python code/16-current-user-dependency.py
```

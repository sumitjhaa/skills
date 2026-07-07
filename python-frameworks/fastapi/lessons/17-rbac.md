# 🛡️ Role-Based Access Control
<!-- ⏱️ 15 min | 🟢 Supplement -->

**What You'll Learn:** Roles, permissions, resource ownership, reusable permission checks.

## Permission Model

```python
PERMISSIONS = {
    "reader": {"read:post"},
    "writer": {"read:post", "write:post"},
    "editor": {"read:post", "write:post", "delete:post"},
    "admin": {"read:post", "write:post", "delete:post", "admin:users"},
}

def has_permission(role: str, permission: str) -> bool:
    return permission in PERMISSIONS.get(role, set())
```

## Permission Dependency

```python
def require_permission(permission: str):
    def checker(current_user: User = Depends(get_current_active_user)):
        if not has_permission(current_user.role, permission):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return checker
```

## Using Permission Checks

```python
@app.get("/admin/users")
def list_users(admin: User = Depends(require_permission("admin:users"))):
    return db.get_all_users()

@app.post("/posts")
def create_post(user: User = Depends(require_permission("write:post"))):
    return db.create_post(user.id)

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, user: User = Depends(require_permission("delete:post"))):
    post = db.get_post(post_id)
    if post.user_id != user.id and "admin:users" not in PERMISSIONS[user.role]:
        raise HTTPException(status_code=403, detail="Not your post")
    return db.delete_post(post_id)
```

## Resource Ownership

Check that a user can only modify their own resources:

```python
def can_modify_post(post_id: int, user: User):
    post = db.get_post(post_id)
    if post is None:
        raise HTTPException(404)
    if post.user_id != user.id and not has_permission(user.role, "admin:users"):
        raise HTTPException(403, detail="Not your post")
    return post
```

## Run the Code

```bash
python code/17-rbac.py
```

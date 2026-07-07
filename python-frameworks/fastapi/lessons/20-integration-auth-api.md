# 🏁 Integration: Full Auth API
<!-- ⏱️ 20 min | 🟢 Challenge -->

**What You'll Learn:** Combine JWT auth, RBAC, SQLAlchemy, file uploads, and testing into one API.

## Features

- User registration & login with JWT
- Role-based access (user, moderator, admin)
- Full CRUD for posts with ownership checks
- Comment system on posts
- File upload with permission check
- Admin endpoints for user management
- Health check endpoint

## Endpoints

| Method | Path | Permissions |
|--------|------|-------------|
| `POST` | `/auth/register` | Public |
| `POST` | `/auth/login` | Public |
| `GET` | `/auth/me` | Any authenticated |
| `POST` | `/posts` | `write:post` |
| `GET` | `/posts` | Public |
| `GET` | `/posts/{id}` | Public |
| `DELETE` | `/posts/{id}` | `delete:post` + ownership |
| `POST` | `/posts/{id}/comments` | `write:comment` |
| `POST` | `/upload` | `upload:file` |
| `GET` | `/admin/users` | `admin:users` |
| `GET` | `/health` | Public |

## Architecture

```
Client → FastAPI → Auth Middleware (JWT)
                  → Permission Check (RBAC)
                  → Business Logic (CRUD)
                  → Database (In-memory / SQLAlchemy)
```

## Patterns Used

| Pattern | Where |
|---------|-------|
| JWT tokens | `/auth/register`, `/auth/login` |
| Dependency chain | `require_auth` → `require_permission` |
| RBAC | `rbac.check(role, permission)` |
| Resource ownership | Post deletion checks `user_id` |
| File upload | `/upload` with extension validation |
| Admin isolation | `/admin/*` requires `admin:users` |

## Running

```bash
python code/20-integration-auth-api.py
```

<!-- 🎯 This is the blueprint for every real-world FastAPI project. Master each piece. -->

# 🏋️ FastAPI Practice — Phase 02

## 1. 🟢 SQLAlchemy Models
Define `Author` and `Book` SQLAlchemy models. Author: `id`, `name`, `bio`. Book: `id`, `title`, `year`, `author_id` (FK). Create endpoints: `POST /authors`, `GET /authors`, `GET /authors/{id}` with their books.

## 2. 🟡 Alembic Migration
Write an Alembic migration that adds a `published_date` column (Date type) to the `books` table. Write both `upgrade()` and `downgrade()`. Verify with `alembic history`.

## 3. 🟡 Async Queries
Create async endpoints for `GET /books` and `GET /books/{id}` using an async database pool. Simulate 10 concurrent requests and verify they all complete.

## 4. 🟢 JWT Auth
Implement register and login endpoints that return JWT tokens. Create a protected `GET /profile` endpoint that returns the current user from the token. Test with valid and expired tokens.

## 5. 🟡 OAuth2 Password Flow
Add a `/token` endpoint supporting `grant_type=password` with scopes. Create users with `read` and `write` scopes. Enforce that `POST /books` requires `write` scope.

## 6. 🟡 Current User Dependency
Create reusable dependencies: `get_token_payload`, `get_current_user`, `get_current_active_user`. Chain them so `GET /profile` uses the full chain. Test that inactive users get rejected.

## 7. 🟡 RBAC
Implement roles: `viewer` (read books), `contributor` (add/edit books), `admin` (delete books + manage users). Create endpoints for each permission level. Test ownership checks for edits.

## 8. 🟢 File Upload
Create `POST /upload/avatar` that accepts images only (jpg, png, webp, max 2MB). Return the URL. Validate extension and size before saving.

## 9. 🟡 Testing
Write pytest-style tests for: `GET /books` returns list, `POST /books` creates a book, `POST /books` rejects unauthenticated requests, `DELETE /books/{id}` checks ownership, health endpoint returns 200. Use fixtures for DB setup.

## 10. 🔴 Complete Library API with Auth
Build a full Library API combining everything:
- `Author` and `Book` models with relationships
- Alembic migration for schema
- JWT auth with register/login
- RBAC: librarian (full CRUD), member (read + borrow), guest (read only)
- File upload for book covers (images only, 5MB max)
- Comments/reviews on books
- Admin endpoints for user management
- Test suite with fixtures
- Health check endpoint

# 🏋️ Flask Practice — Phase 02

## 1. 🟡 User Auth
Build a complete auth system with Flask-Login: registration (username, email, password with hashing), login, logout, profile page (protected), password change. Use `@login_required` and `current_user`.

## 2. 🟡 REST API
Build a RESTful API for a library:
- `GET /api/books` — list all (with pagination: `?page=1&limit=10`)
- `GET /api/books/<id>` — get single
- `POST /api/books` — create (validate title, author, year)
- `PUT /api/books/<id>` — update
- `DELETE /api/books/<id>` — delete
Return proper HTTP status codes and error messages.

## 3. 🟡 File Uploads
Create a profile picture upload endpoint: validate file type (jpg, png, gif only), max size (5MB), save with hashed filename. Add `GET /uploads/<filename>` to serve files. Add a gallery endpoint for multiple file upload.

## 4. 🟡 Email
Build a newsletter system: `POST /newsletter/subscribe` (stores email + sends confirmation), `POST /newsletter/send` (bulk send to all subscribers), welcome email template. Track sent status and history.

## 5. 🟡 Background Tasks
Build a report generation system: queue report generation (slow simulation), check status at `GET /reports/<id>`, list all reports with their statuses, stats endpoint showing completed/failed/pending counts.

## 6. 🟡 Testing
Write pytest tests for a todo list API:
- Test list, create, get, delete endpoints
- Test validation (empty title, negative priority)
- Test 404 for non-existent todos
- Use fixtures for test data setup
- Run with coverage and achieve >90%

## 7. 🟡 Caching
Implement caching for a product catalog:
- Cache product list (TTL 60s, tag-based)
- Cache individual product (TTL 120s)
- Invalidate on create/update/delete
- Add cache stats endpoint
- Measure and display hit rate before and after invalidation

## 8. 🟡 Deployment
Create a deployment configuration for your app:
- Config classes for dev/staging/production
- Gunicorn config (workers, timeout, bind)
- Nginx config with SSL, rate limiting, static serving
- Environment variable setup
- `systemd` service file

## 9. 🟡 Docker
Containerize your Flask app:
- Multi-stage Dockerfile (builder + runner)
- docker-compose with web, postgres, redis, nginx services
- Named volumes for database persistence
- Environment variables for secrets
- Healthcheck configuration

## 10. 🔴 Full Production App
Build a complete production-grade e-commerce API:
- User auth with password hashing and roles (admin/customer)
- Product CRUD with caching
- Shopping cart (session-based)
- Order placement with stock management
- Background email confirmation
- Admin dashboard with stats
- File upload for product images
- Docker Compose setup
- Rate limiting on auth endpoints
- Health check and metrics endpoint

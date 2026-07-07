# 🏋️ FastAPI Practice — Phase 03

## 1. 🟡 Background Tasks
Create a `POST /orders` endpoint that processes an order (store in DB) and sends a confirmation email via `BackgroundTasks`. Add a `GET /tasks/{id}` to check task status. Test with 3 concurrent orders.

## 2. 🟡 WebSocket Chat
Build a WebSocket chat room with: connect to room, send message, broadcast to others, disconnect. Add room listing and message history (last 50 messages). Simulate 5 users chatting.

## 3. 🟡 Rate Limiting
Implement rate limiting on `POST /login`: max 5 attempts per IP per minute using sliding window. Return 429 with `Retry-After` header when exceeded. Test by sending 10 rapid requests.

## 4. 🟡 Async SQLAlchemy
Refactor a sync CRUD API to async SQLAlchemy 1.4+. Convert all `session.query()` to `await session.execute(select(...))`. Verify all endpoints still work.

## 5. 🟢 OpenAPI Customization
Add custom metadata to your API: title, description, version, contact info. Add `operation_id` and `tags` to every endpoint. Add a custom 404 response schema. Verify in `/openapi.json`.

## 6. 🟡 Docker Compose
Create a Dockerfile and docker-compose.yml for a FastAPI app with: multi-stage build, PostgreSQL service, Redis service, health checks, named volumes, and a custom network.

## 7. 🟡 CI/CD Pipeline
Write a GitHub Actions workflow with: lint (ruff), type check (mypy), test (pytest), build (Docker), and deploy (to staging on PR merge, production on manual trigger).

## 8. 🟢 Performance
Profile your API: add a slow endpoint (a loop with 100 DB queries) and a cached version. Compare response times. Calculate speedup. Show cache hit rate.

## 9. 🟡 Monitoring
Implement structured logging (JSON format), metrics (request count + duration), and health checks (DB, Redis, disk). Write an alert rule that triggers when error rate > 5%.

## 10. 🔴 Complete Production API
Build a full production API combining everything:
- Background tasks for email + report generation
- WebSocket notifications for real-time events
- Rate limiting per IP/user/endpoint
- Async SQLAlchemy with connection pooling
- Docker Compose with all services
- CI/CD pipeline with 4 stages
- Caching with TTL for frequent queries
- Structured logging + metrics + health checks
- OpenAPI schema with full metadata
- At least 5 error scenarios handled gracefully

# ⚡ FastAPI — Modern Async APIs

Build production-ready REST APIs with FastAPI: auto-docs, Pydantic validation, dependency injection, async support.

## Progress

### Phase 01 — FastAPI Foundations ✅
| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 01 | [Project Setup & First Endpoint](lessons/01-project-setup.md) | [01-project-setup.py](code/01-project-setup.py) | App creation, uvicorn, auto-docs |
| 02 | [Path & Query Parameters](lessons/02-path-query-params.md) | [02-path-query-params.py](code/02-path-query-params.py) | Path params, query params, coercion |
| 03 | [Request Body & Pydantic](lessons/03-request-body-pydantic.md) | [03-request-body-pydantic.py](code/03-request-body-pydantic.py) | Pydantic models, field validation |
| 04 | [Response Models](lessons/04-response-models.md) | [04-response-models.py](code/04-response-models.py) | response_model, status codes |
| 05 | [Error Handling](lessons/05-error-handling.md) | [05-error-handling.py](code/05-error-handling.py) | HTTPException, custom handlers |
| 06 | [Dependencies](lessons/06-dependencies.md) | [06-dependencies.py](code/06-dependencies.py) | Depends, shared resources, DAG |
| 07 | [Middleware & CORS](lessons/07-middleware-cors.md) | [07-middleware-cors.py](code/07-middleware-cors.py) | Custom middleware, CORS config |
| 08 | [Routers](lessons/08-routers.md) | [08-routers.py](code/08-routers.py) | APIRouter, modular organization |
| 09 | [Static Files & Templates](lessons/09-static-templates.md) | [09-static-templates.py](code/09-static-templates.py) | StaticFiles, Jinja2 templates |
| 10 | [Integration: Blog API](lessons/10-integration-blog-api.md) | [10-integration-blog-api.py](code/10-integration-blog-api.py) | Full CRUD, all patterns combined |

### Phase 02 — Database & Auth ✅
| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 11 | [SQLAlchemy + FastAPI](lessons/11-sqlalchemy-models.md) | [11-sqlalchemy-models.py](code/11-sqlalchemy-models.py) | Models, sessions, CRUD patterns |
| 12 | [Alembic Migrations](lessons/12-alembic-migrations.md) | [12-alembic-migrations.py](code/12-alembic-migrations.py) | Schema versioning, upgrade/downgrade |
| 13 | [Async DB with asyncpg](lessons/13-async-db-asyncpg.md) | [13-async-db-asyncpg.py](code/13-async-db-asyncpg.py) | Connection pool, async queries |
| 14 | [JWT Authentication](lessons/14-jwt-auth.md) | [14-jwt-auth.py](code/14-jwt-auth.py) | Token creation, verification, expiration |
| 15 | [OAuth2 & Password Flow](lessons/15-oauth2-password-flow.md) | [15-oauth2-password-flow.py](code/15-oauth2-password-flow.py) | /token endpoint, scopes, hashing |
| 16 | [Current User Dependency](lessons/16-current-user-dependency.md) | [16-current-user-dependency.py](code/16-current-user-dependency.py) | Auth extraction, dependency chaining |
| 17 | [Role-Based Access Control](lessons/17-rbac.md) | [17-rbac.py](code/17-rbac.py) | Permissions, roles, ownership checks |
| 18 | [File Uploads](lessons/18-file-uploads.md) | [18-file-uploads.py](code/18-file-uploads.py) | UploadFile, validation, storage |
| 19 | [Testing with httpx + pytest](lessons/19-testing-httpx-pytest.md) | [19-testing-httpx-pytest.py](code/19-testing-httpx-pytest.py) | TestClient, fixtures, assertions |
| 20 | [Integration: Full Auth API](lessons/20-integration-auth-api.md) | [20-integration-auth-api.py](code/20-integration-auth-api.py) | All patterns combined |

### Phase 03 — Advanced & Production ✅
| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 21 | [Background Tasks](lessons/21-background-tasks.md) | [21-background-tasks.py](code/21-background-tasks.py) | BackgroundTasks, deferred execution |
| 22 | [WebSockets](lessons/22-websockets.md) | [22-websockets.py](code/22-websockets.py) | Real-time connections, broadcast, rooms |
| 23 | [Rate Limiting](lessons/23-rate-limiting.md) | [23-rate-limiting.py](code/23-rate-limiting.py) | Token bucket, sliding window, per-IP |
| 24 | [Async SQLAlchemy](lessons/24-async-sqlalchemy.md) | [24-async-sqlalchemy.py](code/24-async-sqlalchemy.py) | Async engine, sessions, async CRUD |
| 25 | [OpenAPI Customization](lessons/25-openapi-customization.md) | [25-openapi-customization.py](code/25-openapi-customization.py) | Schema metadata, tags, examples |
| 26 | [Docker + Docker Compose](lessons/26-docker-compose.md) | [26-docker-compose.py](code/26-docker-compose.py) | Multi-stage builds, services, volumes |
| 27 | [CI/CD for APIs](lessons/27-cicd.md) | [27-cicd.py](code/27-cicd.py) | Pipelines, GitHub Actions, deploy |
| 28 | [Performance Tuning](lessons/28-performance-tuning.md) | [28-performance-tuning.py](code/28-performance-tuning.py) | Profiling, caching, N+1, connection pool |
| 29 | [Monitoring & Logging](lessons/29-monitoring-logging.md) | [29-monitoring-logging.py](code/29-monitoring-logging.py) | Structured logs, metrics, health checks |
| 30 | [Integration: Production API](lessons/30-integration-production-api.md) | [30-integration-production-api.py](code/30-integration-production-api.py) | All patterns combined |

## Practice
- [Phase 01 Exercises](practice/phase01-exercises.md)
- [Phase 02 Exercises](practice/phase02-exercises.md)
- [Phase 03 Exercises](practice/phase03-exercises.md)

## Quick Start
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
# http://localhost:8000/docs
```

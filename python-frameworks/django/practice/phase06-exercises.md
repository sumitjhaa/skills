# 🏋️ Django Practice — Phase 06 (Production)

## 1. 🟢 Docker
Write a `Dockerfile` with multi-stage build (builder → runtime). Create a `docker-compose.yml` with `web`, `db` (postgres), `redis`, and `celery` services. Add `.dockerignore`.

## 2. 🟢 CI/CD
Create a GitHub Actions workflow that: lints with `ruff`, runs `pytest`, builds docker images, runs migrations, and deploys to a VPS on `main` branch push.

## 3. 🟡 Deployment
Deploy Django on a VPS with: Nginx reverse proxy, Gunicorn behind systemd, PostgreSQL, Let's Encrypt SSL, and a health check endpoint at `/health/`.

## 4. 🟡 Settings Management
Split settings into `base.py`, `development.py`, `staging.py`, `production.py`. Use `django-environ` to load from `.env`. Validate that production refuses to start without `SECRET_KEY`.

## 5. 🟡 Logging
Configure structured JSON logging. Add `RotatingFileHandler` with 10MB max size. Send Django request logs to a file. Configure Sentry for error tracking.

## 6. 🟡 Security
Run `python manage.py check --deploy` and fix all warnings. Add CSP headers with `django-csp`. Enable rate limiting. Set `PASSWORD_HASHERS` to use Argon2.

## 7. 🟡 Database Migrations
Create a migration to add `slug` to a model. Write a reversible `RunPython` data migration. Write a backup script with `pg_dump` → gzip → S3.

## 8. 🟡 Performance Monitoring
Install `django-debug-toolbar` and verify query count. Add `pg_stat_statements` to PostgreSQL. Set up Sentry APM with `traces_sample_rate=0.1`.

## 9. 🟡 Error Tracking
Configure Sentry with Django + Celery integrations. Capture an intentional error with user context. Set up Slack alerts for errors, PagerDuty for criticals.

## 10. 🔴 Full Production Deployment
Combine everything:
- Docker compose with web, db, redis, celery
- GitHub Actions CI/CD pipeline
- Production settings with env vars
- Sentry error tracking + structured logging
- All security settings enabled
- Database backups automated
- Health check endpoint
- Monitoring dashboard (Grafana)
- Written runbook for deploy, rollback, backup, and incidents

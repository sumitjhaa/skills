# 📘 Django Phase 06 — Lesson 10: Integration — Full Production Deployment

> 🎯 **Goal**: Combine all Phase 06 concepts into a complete production deployment pipeline.

## 📖 Concepts

### What We're Building
A fully automated production deployment with:
- Docker containers for all services
- CI/CD pipeline (test → build → deploy)
- Environment-specific settings with secrets management
- Structured logging + Sentry error tracking
- Security hardening (HTTPS, CSP, rate limiting)
- Database backup automation
- Health checks + monitoring
- Production runbook

### Deployment Architecture
```
GitHub                    VPS / Cloud
┌────────┐   push         ┌────────────────────────┐
│  Code   ├──────────────→│   GitHub Actions        │
└────────┘                │   ├─ lint, test         │
                          │   ├─ docker build        │
                          │   └─ deploy via SSH      │
                          └────────┬───────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │      Docker Compose          │
                    ├─────────────────────────────┤
                    │  Nginx (443) ←─→ Web (8000) │
                    │         ↓                    │
                    │  Static (S3)  DB (5432)      │
                    │  Redis (6379)  Celery        │
                    └─────────────────────────────┘
```

### Production Checklist
```
Pre-deploy:
  ☐ Tests pass (CI)
  ☐ Migrations tested on staging
  ☐ Backup created
  ☐ Release notes written

Deploy:
  ☐ Pull latest code
  ☐ Build Docker images
  ☐ Run migrations
  ☐ Collect static files
  ☐ Restart services
  ☐ Verify health check

Post-deploy:
  ☐ Check Sentry for new errors
  ☐ Verify monitoring dashboard
  ☐ Confirm backups still running
  ☐ Notify team
```

### Runbook
A runbook documents what to do in common scenarios:
- **Deploy**: `docker compose up -d --build`
- **Rollback**: `docker compose up -d web=previous_version`
- **Scale**: `docker compose up -d --scale web=5`
- **DB restore**: `psql < backup.sql`
- **View logs**: `docker compose logs -f web`
- **Restart Celery**: `docker compose restart celery`

### ADHD-Friendly Summary
```
CI/CD: push → test → build → deploy
Docker: compose up → everything running
Backup: pg_dump daily → S3
Monitor: Sentry + health checks
Runbook: documented recovery steps
```

## 🛠️ Code

```python
# deploy/runbook.py
RUNBOOK = {
    "deploy": {
        "steps": [
            "git pull origin main",
            "docker compose build",
            "docker compose run --rm web python manage.py migrate",
            "docker compose run --rm web python manage.py collectstatic --noinput",
            "docker compose up -d --force-recreate",
            "sleep 5 && curl -f http://localhost:8000/health/",
        ],
        "rollback": "docker compose up -d web_previous",
    },
    "backup": {
        "db": "pg_dump -h localhost -U myapp myapp | gzip > backup_$(date +%Y%m%d).sql.gz",
        "upload": "aws s3 cp backup.sql.gz s3://backups/",
        "restore": "gunzip -c backup.sql.gz | psql -h localhost -U myapp myapp",
    },
    "monitoring": {
        "logs": "docker compose logs -f --tail=100 web",
        "health": "curl -f http://localhost:8000/health/",
        "metrics": "curl http://localhost:8000/metrics/",
    },
    "incident": {
        "1": "Check Sentry for error details",
        "2": "Check logs: docker compose logs --tail=200 web",
        "3": "Check database: docker compose exec db pg_isready",
        "4": "Check Redis: docker compose exec redis redis-cli ping",
        "5": "If needed, rollback: docker compose up -d web_previous",
        "6": "Notify team in Slack",
    },
}
```

## 🧪 Practice

Build the complete production deployment:

1. **Docker**: Dockerfile + docker-compose.yml for all services
2. **CI/CD**: GitHub Actions workflow (test → build → deploy)
3. **Settings**: Separate dev/staging/production settings with env vars
4. **Security**: Enable all Django security settings + CSP + rate limiting
5. **Error tracking**: Sentry with Django integration
6. **Logging**: Structured JSON logs with rotation
7. **Backups**: Automated pg_dump to S3
8. **Health check**: `/health/` endpoint checking all services
9. **Runbook**: Document deploy, rollback, backup, and incident steps
10. **Monitoring**: Verify health check, logs, and error tracking work

## 🧠 Key Takeaways

- Automate everything — deploys should be one command
- CI/CD catches issues before they reach production
- Docker ensures environment consistency
- Monitoring tells you about problems before users do
- A runbook saves precious minutes during incidents
- Test your disaster recovery — can you actually restore from backup?
- Security is not a feature — it's a continuous practice

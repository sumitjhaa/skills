# 🌶️ Flask — Web Apps & APIs

Build web applications and REST APIs with Flask: Jinja2 templates, SQLAlchemy, blueprints, Flask-Login, Flask-WTF, and production deployment.

## Progress

### Phase 01 — Flask Foundations ✅
| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 01 | [Project Setup & First Routes](lessons/01-project-setup.md) | [01-project-setup.py](code/01-project-setup.py) | App creation, routes, dev server |
| 02 | [Jinja2 Templates](lessons/02-templates.md) | [02-templates.py](code/02-templates.py) | Rendering, variables, filters, inheritance |
| 03 | [Static Files](lessons/03-static-files.md) | [03-static-files.py](code/03-static-files.py) | CSS, JS, images, url_for |
| 04 | [Request Handling](lessons/04-request-handling.md) | [04-request-handling.py](code/04-request-handling.py) | Query params, form data, headers, methods |
| 05 | [Forms & WTForms](lessons/05-forms-wtf.md) | [05-forms-wtf.py](code/05-forms-wtf.py) | Form classes, validation, CSRF |
| 06 | [Database with SQLAlchemy](lessons/06-database-sqlalchemy.md) | [06-database-sqlalchemy.py](code/06-database-sqlalchemy.py) | Models, CRUD, relationships, queries |
| 07 | [Blueprints](lessons/07-blueprints.md) | [07-blueprints.py](code/07-blueprints.py) | Modular apps, URL prefixes, organization |
| 08 | [Error Handling](lessons/08-error-handling.md) | [08-error-handling.py](code/08-error-handling.py) | abort(), custom handlers, error pages |
| 09 | [Flash Messages & Sessions](lessons/09-flash-sessions.md) | [09-flash-sessions.py](code/09-flash-sessions.py) | Session storage, flash, temporary data |
| 10 | [Integration: Blog App](lessons/10-integration-blog.md) | [10-integration-blog.py](code/10-integration-blog.py) | Full CRUD blog with auth, comments |

### Phase 02 — Production Features ✅
| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 11 | [User Authentication](lessons/11-user-auth.md) | [11-user-auth.py](code/11-user-auth.py) | Flask-Login, password hashing, login_required |
| 12 | [REST API](lessons/12-rest-api.md) | [12-rest-api.py](code/12-rest-api.py) | Resources, request parsing, marshalling |
| 13 | [File Uploads](lessons/13-file-uploads.md) | [13-file-uploads.py](code/13-file-uploads.py) | Multipart forms, validation, secure names |
| 14 | [Email with Flask-Mail](lessons/14-email.md) | [14-email.py](code/14-email.py) | Sending, templates, attachments, async |
| 15 | [Background Tasks](lessons/15-background-tasks.md) | [15-background-tasks.py](code/15-background-tasks.py) | Thread pools, job queues, tracking |
| 16 | [Testing with pytest](lessons/16-testing-pytest.md) | [16-testing-pytest.py](code/16-testing-pytest.py) | Test client, fixtures, assertions, coverage |
| 17 | [Caching](lessons/17-caching.md) | [17-caching.py](code/17-caching.py) | In-memory cache, TTL, decorators, invalidation |
| 18 | [Deployment](lessons/18-deployment.md) | [18-deployment.py](code/18-deployment.py) | Gunicorn, Nginx, env configs |
| 19 | [Docker](lessons/19-docker.md) | [19-docker.py](code/19-docker.py) | Dockerfile, compose, multi-stage builds |
| 20 | [Integration: Production App](lessons/20-integration-production.md) | [20-integration-production.py](code/20-integration-production.py) | Auth, API, caching, Docker combined |

## Practice
- [Phase 01 Exercises](practice/phase01-exercises.md)
- [Phase 02 Exercises](practice/phase02-exercises.md)

## Quick Start
```bash
pip install flask
flask run --debug
# http://127.0.0.1:5000
```

# 📘 Django Phase 06 — Lesson 06: Security Hardening

> 🎯 **Goal**: Secure a Django application — HTTPS, CSP, SQL injection prevention, rate limiting, and common vulnerabilities.

## 📖 Concepts

### Django Security Settings

```python
# Must-haves for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Common Vulnerabilities & Protections

| Vulnerability | Django Protection | Additional |
|---------------|-------------------|------------|
| **SQL Injection** | ORM parameterizes queries | Never use raw SQL with string formatting |
| **XSS** | Template auto-escapes | CSP headers, `mark_safe` carefully |
| **CSRF** | `CsrfViewMiddleware` | `CSRF_TRUSTED_ORIGINS` for CORS |
| **Clickjacking** | `X-Frame-Options: DENY` | `django.middleware.clickjacking.XFrameOptionsMiddleware` |
| **Host header** | `ALLOWED_HOSTS` validation | Never use `ALLOWED_HOSTS = ['*']` |
| **Mass assignment** | `fields` in ModelForms/Serializers | Never use `fields = '__all__'` with user input |

### Content Security Policy (CSP)
```python
# With django-csp middleware
CSP_DEFAULT_SRC = ["'self'"]
CSP_SCRIPT_SRC = ["'self'", "'unsafe-inline'", "cdn.example.com"]
CSP_STYLE_SRC = ["'self'", "'unsafe-inline'"]
CSP_IMG_SRC = ["'self'", "data:", "https:"]
CSP_FRAME_ANCESTORS = ["'none'"]
```

### Rate Limiting
```python
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}
```

### Password Security
```python
# Use bcrypt or argon2
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
]
```

### ADHD-Friendly Summary
```
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSP headers → prevent XSS
Rate limiting → prevent abuse
Argon2 → strongest password hashing
ALLOWED_HOSTS → prevent host header attacks
```

## 🛠️ Code

```python
# settings.py — security checklist
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Rate limiting
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}
```

## 🧪 Practice

1. Enable all security settings in production
2. Add CSP headers with `django-csp`
3. Configure rate limiting for API endpoints
4. Run `python manage.py check --deploy` and fix all warnings
5. Set up password validation with Argon2 hasher

## 🧠 Key Takeaways

- `python manage.py check --deploy` lists all security issues
- HTTPS is non-negotiable — redirect all HTTP to HTTPS
- CSP prevents XSS even if a script tag slips through
- Rate limit everything, especially auth endpoints
- Use `django-csp`, `django-cors-headers`, `django-ratelimit` packages
- Audit dependencies regularly with `pip-audit` or `safety`

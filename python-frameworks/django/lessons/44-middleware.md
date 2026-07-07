# 📘 Django Phase 05 — Lesson 04: Middleware

> 🎯 **Goal**: Process requests globally — timing, security headers, IP blocking, authentication checks.

## 📖 Concepts

### What Is Middleware?
A lightweight plugin system for request/response processing. Each middleware is a callable that processes every request before it reaches the view and every response before it leaves.

### Middleware Flow
```
Request → Middleware 1 → Middleware 2 → ... → View → ... → Middleware 2 → Middleware 1 → Response
                     (process_request)                  (process_response)
```

### Hook Methods

| Method | Purpose | Return |
|--------|---------|--------|
| `process_request(request)` | Before view | `None` or `HttpResponse` |
| `process_response(request, response)` | Before response | `HttpResponse` |
| `process_view(request, view_func, args, kwargs)` | Before view but after request | `None` or `HttpResponse` |
| `process_exception(request, exception)` | On unhandled exception | `None` or `HttpResponse` |
| `process_template_response(request, response)` | For `TemplateResponse` | `TemplateResponse` |

### Common Middleware

| Middleware | Purpose |
|------------|---------|
| `SecurityMiddleware` | HTTPS redirect, HSTS, XSS protection |
| `SessionMiddleware` | Session management |
| `AuthenticationMiddleware` | `request.user` from session |
| `CommonMiddleware` | URL normalization, `APPEND_SLASH` |
| `CsrfViewMiddleware` | CSRF protection |
| `GZipMiddleware` | Response compression |
| `LocaleMiddleware` | Language detection |

### Custom Middleware Order
Middleware in `MIDDLEWARE` list runs top-to-bottom on request, bottom-to-top on response.

### ADHD-Friendly Summary
```
process_request() → pre-view hook
process_response() → post-view hook
process_exception() → catch errors
Return None to pass through; return Response to short-circuit
```

## 🛠️ Code

```python
# middleware.py
import time

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        response['X-Duration'] = f'{duration:.3f}s'
        return response


class BlockPrivateIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip and ip.startswith(('10.', '172.16.', '192.168.')):
            return HttpResponseForbidden('Private IPs not allowed')
        return self.get_response(request)


# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'myapp.middleware.RequestTimingMiddleware',
    'myapp.middleware.BlockPrivateIPMiddleware',
    # ... built-in middleware
]
```

## 🧪 Practice

1. Create a `RequestTimingMiddleware` that logs duration to console
2. Create a `AdminIPWhitelistMiddleware` that restricts `/admin/` to specific IPs
3. Create a `SecurityHeadersMiddleware` that adds `X-Content-Type-Options: nosniff`
4. Create an `ErrorHandlingMiddleware` that catches `DoesNotExist` and returns 404
5. Reorder middleware and observe behavior changes

## 🧠 Key Takeaways

- Middleware runs in order — first listed = first processed on request
- Return `HttpResponse` early to short-circuit (block, redirect, etc.)
- `process_exception` only catches unhandled exceptions from views
- Keep middleware fast — it runs on every request
- Use middleware for cross-cutting concerns (security, logging, timing)

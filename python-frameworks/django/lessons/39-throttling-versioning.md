# 📘 Django Phase 04 — Lesson 09: Throttling & Versioning

> 🎯 **Goal**: Rate-limit API requests and manage API versioning strategies.

## 📖 Concepts

### Throttling
Control how many requests a client can make in a given time window.

| Throttle Class | Scope | Default Rate |
|----------------|-------|-------------|
| `AnonRateThrottle` | Unauthenticated users | `None` (configure in settings) |
| `UserRateThrottle` | Authenticated users | `None` |
| `ScopedRateThrottle` | Per-view scope | `None` |

### Configuration
```python
# settings.py
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

### Per-View Throttling
```python
class UploadView(APIView):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'uploads'

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'uploads': '10/minute',
    },
}
```

### Response on Throttle
429 Too Many Requests:
```json
{"detail": "Request was throttled. Expected available in 32 seconds."}
```

### Versioning
Control API evolution without breaking existing clients.

| Strategy | How | URL Example |
|----------|-----|-------------|
| `URLPathVersioning` | Path prefix | `/api/v1/posts/` |
| `AcceptHeaderVersioning` | Accept header | `Accept: application/json; version=v2` |
| `QueryParameterVersioning` | Query param | `/api/posts/?version=v2` |
| `HostNameVersioning` | Subdomain | `v1.api.example.com` |
| `NamespaceVersioning` | URL namespace | (uses reverse) |

### URL Path Versioning
```python
# urls.py
urlpatterns = [
    path('api/v1/', include('posts.v1_urls')),
    path('api/v2/', include('posts.v2_urls')),
]
```

### Accept Header Versioning
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

### ADHD-Friendly Summary
```
Throttle → rate limit by user type
Versioning → v1, v2 in URL or Accept header
'10/minute', '100/hour', '1000/day'
request.version available in views
```

## 🛠️ Code

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '100/minute',
    },
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}

# versioned views
class PostListV1(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerV1  # flat author

class PostListV2(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerV2  # nested author
```

## 🧪 Practice

1. Set `AnonRateThrottle` to `5/minute` — make 7 requests, check 429 on the 6th
2. Create a scoped throttle `'burst': '3/second'`
3. Implement URL path versioning: `/api/v1/books/` and `/api/v2/books/`
4. Create `BookSerializerV1` (flat author id) and `BookSerializerV2` (nested author)
5. Use `AcceptHeaderVersioning` and test with curl

## 🧠 Key Takeaways

- Throttling prevents abuse — always set `DEFAULT_THROTTLE_RATES`
- Rates use format: `{count}/{period}` where period = second, minute, hour, day
- Version your API from day 1 — even if only v1 exists
- URL path versioning is simplest for most projects
- Use `request.version` to conditionally return different data

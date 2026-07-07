"""View concepts — pure Python simulation."""
from dataclasses import dataclass, field


@dataclass
class HttpRequest:
    method: str = 'GET'
    path: str = '/'
    GET: dict = field(default_factory=dict)
    POST: dict = field(default_factory=dict)


@dataclass
class HttpResponse:
    content: str = ''
    status_code: int = 200
    content_type: str = 'text/html'


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse(content="<h1>Welcome to my blog!</h1>")


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    posts = {
        'hello-django': {'title': 'Hello Django', 'content': 'First post!'},
        'django-models': {'title': 'Django Models', 'content': 'Second post!'},
    }
    post = posts.get(slug)
    if not post:
        return HttpResponse(content="Not found", status_code=404)
    content = f"<h1>{post['title']}</h1><p>{post['content']}</p>"
    return HttpResponse(content=content)


req = HttpRequest(path='/')
resp = home(req)
print(f"GET {req.path} → {resp.status_code}")
print(resp.content[:50])

req2 = HttpRequest(path='/posts/hello-django/')
resp2 = post_detail(req2, 'hello-django')
print(f"\nGET {req2.path} → {resp2.status_code}")
print(resp2.content)

req3 = HttpRequest(path='/posts/nonexistent/')
resp3 = post_detail(req3, 'nonexistent')
print(f"\nGET {req3.path} → {resp3.status_code}")
print(resp3.content)

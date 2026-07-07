"""Class-based views — pure Python simulation."""
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class HttpRequest:
    user: str = 'anonymous'
    method: str = 'GET'


@dataclass
class HttpResponse:
    content: str = ''
    status: int = 200


class View:
    """Base class-based view."""
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        handler = getattr(self, request.method.lower(), None)
        if handler is None:
            return HttpResponse(content="Method not allowed", status=405)
        return handler(request, *args, **kwargs)

    @classmethod
    def as_view(cls) -> Callable:
        def view(request, *args, **kwargs):
            instance = cls()
            return instance.dispatch(request, *args, **kwargs)
        return view


class ListView(View):
    model_name: str = 'items'
    items: list = field(default_factory=list)

    def get(self, request):
        items_str = '\n'.join(f"  - {item}" for item in self.items)
        return HttpResponse(content=f"{self.model_name}:\n{items_str}")


class DetailView(View):
    item: str = ''

    def get(self, request, **kwargs):
        return HttpResponse(content=f"Detail: {self.item}")


# Subclass with concrete data
class PostListView(ListView):
    model_name = 'Posts'
    items = ['Hello Django', 'Django Models', 'Django Views']


class PostDetailView(DetailView):
    def get(self, request, **kwargs):
        posts = {'hello-django': 'First post!', 'django-models': 'Second post!'}
        slug = kwargs.get('slug', '')
        content = posts.get(slug, 'Not found')
        return HttpResponse(content=f"Post '{slug}': {content}")


# Usage
list_view = PostListView.as_view()
print(list_view(HttpRequest()).content)

detail_view = PostDetailView.as_view()
print(detail_view(HttpRequest(), slug='hello-django').content)

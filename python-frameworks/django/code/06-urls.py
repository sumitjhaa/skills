"""URL routing — pure Python simulation."""
import re
from typing import Callable, Optional


def post_detail(slug: str) -> str:
    return f"Viewing post: {slug}"


def archive(year: str, month: str) -> str:
    return f"Archive: {year}-{month}"


def add_comment(slug: str) -> str:
    return f"Comment on: {slug}"


routes = [
    (r'^post/(?P<slug>[-\w]+)/$', post_detail),
    (r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$', archive),
    (r'^post/(?P<slug>[-\w]+)/comment/$', add_comment),
]

test_paths = [
    'post/hello-django/',
    'archive/2024/01/',
    'post/hello-django/comment/',
    'nonexistent/',
]

for path in test_paths:
    matched = False
    for pattern, view in routes:
        match = re.match(pattern, path)
        if match:
            result = view(**match.groupdict())
            print(f"  {path:40s} → {result}")
            matched = True
            break
    if not matched:
        print(f"  {path:40s} → 404 Not Found")

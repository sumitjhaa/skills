"""Web & APIs — urllib and requests for REST APIs.
Run: python 10-03-web-apis.py
"""

import json
from urllib.request import urlopen, Request

BASE_URL = "https://jsonplaceholder.typicode.com"


def get_posts() -> list[dict]:
    with urlopen(f"{BASE_URL}/posts") as resp:
        return json.loads(resp.read())


def get_post(post_id: int) -> dict:
    with urlopen(f"{BASE_URL}/posts/{post_id}") as resp:
        return json.loads(resp.read())


def create_post(title: str, body: str, user_id: int = 1) -> dict:
    data = json.dumps({"title": title, "body": body, "userId": user_id}).encode()
    req = Request(f"{BASE_URL}/posts", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urlopen(req) as resp:
        return json.loads(resp.read())


posts = get_posts()
print(f"Got {len(posts)} posts from API")

post = get_post(1)
print(f"Post 1: {post['title']}")

new_post = create_post("Async in Python", "asyncio is the future!")
print(f"Created post {new_post['id']}")

"""Nested serializers & relationships in DRF."""
from typing import Any, Optional
import json


# ======================== Core ========================
class Request:
    def __init__(self, method="GET", data=None, user=None):
        self.method = method
        self.data = data or {}
        self.user = user


class Response:
    def __init__(self, data, status=200):
        self.data = data
        self.status = status

    def render(self):
        return json.dumps(self.data, indent=2)


# ======================== Models ========================
DB = {"authors": {}, "posts": {}, "comments": {}}
PK = {"author": 1, "post": 1, "comment": 1}


class Author:
    def __init__(self, name, email):
        self.id = PK["author"]
        self.name = name
        self.email = email
        DB["authors"][self.id] = self
        PK["author"] += 1


class Post:
    def __init__(self, title, content, author):
        self.id = PK["post"]
        self.title = title
        self.content = content
        self.author = author
        DB["posts"][self.id] = self
        PK["post"] += 1


class Comment:
    def __init__(self, text, post, author):
        self.id = PK["comment"]
        self.text = text
        self.post = post
        self.author = author
        DB["comments"][self.id] = self
        PK["comment"] += 1


alice = Author("Alice", "alice@example.com")
bob = Author("Bob", "bob@example.com")

post1 = Post("Hello Django", "Content about Django", alice)
post2 = Post("DRF Nested", "Nested serializers", alice)
post3 = Post("Python Tips", "Python content", bob)

Comment("Great post!", post1, bob)
Comment("Thanks!", post1, alice)
Comment("Nice article", post2, bob)
Comment("Very helpful", post2, alice)


# ======================== Serializers ========================

class AuthorSerializer:
    def to_representation(self, instance: Author) -> dict:
        return {
            "id": instance.id,
            "name": instance.name,
            "email": instance.email,
        }


class CommentSerializer:
    def to_representation(self, instance: Comment) -> dict:
        return {
            "id": instance.id,
            "text": instance.text,
            "author": instance.author.name,
        }


class PostSerializer:
    """Flat serializer (author as ID)."""
    def to_representation(self, instance: Post) -> dict:
        return {
            "id": instance.id,
            "title": instance.title,
            "content": instance.content,
            "author": instance.author.id,
        }


class PostNestedAuthorSerializer:
    """Nested: author object embedded in post."""
    def __init__(self):
        self.author_ser = AuthorSerializer()

    def to_representation(self, instance: Post) -> dict:
        return {
            "id": instance.id,
            "title": instance.title,
            "content": instance.content,
            "author": self.author_ser.to_representation(instance.author),
        }


class PostWithCommentsSerializer:
    """Nested: comments embedded in post."""
    def __init__(self):
        self.comment_ser = CommentSerializer()

    def to_representation(self, instance: Post) -> dict:
        comments = [c for c in DB["comments"].values() if c.post.id == instance.id]
        return {
            "id": instance.id,
            "title": instance.title,
            "content": instance.content,
            "author": instance.author.name,
            "comments": [self.comment_ser.to_representation(c) for c in comments],
            "comment_count": len(comments),
        }


class AuthorWithPostsSerializer:
    """Reverse nested: author with list of posts."""
    def __init__(self):
        self.post_ser = PostSerializer()

    def to_representation(self, instance: Author) -> dict:
        posts = [p for p in DB["posts"].values() if p.author.id == instance.id]
        return {
            "id": instance.id,
            "name": instance.name,
            "email": instance.email,
            "posts": [self.post_ser.to_representation(p) for p in posts],
            "post_count": len(posts),
        }


# ======================== Demo ========================
print("=== Nested Serializers Demo ===\n")

post_ser = PostSerializer()
nested_ser = PostNestedAuthorSerializer()
comments_ser = PostWithCommentsSerializer()
author_posts_ser = AuthorWithPostsSerializer()

# Flat (author = ID)
print("1. Flat (author = ID):")
print(json.dumps(post_ser.to_representation(post1), indent=2))

# Nested (author = object)
print("\n2. Nested Author:")
print(json.dumps(nested_ser.to_representation(post1), indent=2))

# Post with comments
print("\n3. Post with Comments:")
print(json.dumps(comments_ser.to_representation(post1), indent=2))

# Author with posts (reverse nested)
print("\n4. Author with Posts:")
print(json.dumps(author_posts_ser.to_representation(alice), indent=2))

# All posts with nested author
print("\n5. All Posts with Nested Author:")
all_posts_ser = PostNestedAuthorSerializer()
all_posts = [all_posts_ser.to_representation(p) for p in DB["posts"].values()]
print(json.dumps(all_posts, indent=2))

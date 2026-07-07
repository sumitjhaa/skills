# 📘 Django Phase 04 — Lesson 08: Nested Serializers

> 🎯 **Goal**: Represent related models in serializers — nested objects, reverse relations, and writable nested data.

## 📖 Concepts

### Why Nested Serializers?
Flat (author = ID):
```json
{"id": 1, "title": "Hello", "author": 1}
```

Nested (author = object):
```json
{"id": 1, "title": "Hello", "author": {"id": 1, "name": "Alice", "email": "alice@x.com"}}
```

### Types of Nesting

| Pattern | Serializer | Output |
|---------|-----------|--------|
| Flat FK | `PrimaryKeyRelatedField` | Author id |
| Nested FK | `AuthorSerializer()` | Full author object |
| Reverse FK | `PostSerializer(many=True)` | List of posts on author |
| Nested comments | `CommentSerializer(many=True)` | Comments on post |
| Hyperlinked | `HyperlinkedRelatedField` | URL to related resource |

### Read-Only Nested
```python
class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']
```

### Writable Nested
```python
class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = Author.objects.create(**author_data)
        return Post.objects.create(author=author, **validated_data)
```

### Reverse Relations
```python
class AuthorSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'posts']

# Or with a method field
class AuthorSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    def get_post_count(self, obj):
        return obj.posts.count()
```

### ADHD-Friendly Summary
```
Nested read-only → embed related serializer with read_only=True
Nested writable  → override create()/update() to handle nested data
many=True        → for lists (author → posts, post → comments)
SerializerMethodField → custom computed values
```

## 🛠️ Code

```python
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author_name', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'comments', 'comment_count', 'created_at']
```

## 🧪 Practice

1. Create `AuthorSerializer` with nested `books` (reverse FK)
2. Create `BookSerializer` with nested `author` (FK)
3. Add a `SerializerMethodField` for `book_count` on author
4. Make the nested author read-only (prevents client setting author data)
5. Create a writable nested serializer that creates/updates author + post together

## 🧠 Key Takeaways

- Nested serializers embed related objects — client gets full data in one request
- Use `read_only=True` for simple display nesting
- Writable nesting requires custom `create()` / `update()`
- `source='field.subfield'` lets you traverse relationships
- `SerializerMethodField` for custom computed values

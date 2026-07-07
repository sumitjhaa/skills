# 📘 Django Phase 04 — Lesson 01: DRF Serializers

> 🎯 **Goal**: Understand serializers — converting complex data (querysets, model instances) to/from JSON.

## 📖 Concepts

### What is a Serializer?
Serializers convert Django models to JSON (serialization) and JSON back to validated Python dicts (deserialization). They also handle validation.

### Serialization vs Deserialization
```
Serialization:   Model → Python dict → JSON
Deserialization: JSON → Python dict → Validated data → Model
```

### Serializer Types

| Type | Purpose | Auto Fields |
|------|---------|-------------|
| `Serializer` | Manual field definition | No |
| `ModelSerializer` | Auto from model fields | Yes |

### Common Field Types

| Field | Input | Output |
|-------|-------|--------|
| `CharField` | String | String |
| `IntegerField` | int | int |
| `BooleanField` | bool | bool |
| `DateTimeField` | ISO string | datetime |
| `EmailField` | Email string | String |
| `SerializerMethodField` | — | Custom computed |

### Validation
```python
# Field-level
def validate_title(self, value):
    if len(value) < 3:
        raise serializers.ValidationError("Too short")
    return value

# Object-level
def validate(self, data):
    if data['start'] > data['end']:
        raise serializers.ValidationError("Start before end")
    return data
```

### ADHD-Friendly Summary
```
ser = PostSerializer(instance=post)   → .data = dict
ser = PostSerializer(data=json_data)  → .is_valid(), .validated_data
ModelSerializer → auto fields from model
Validation → field-level & object-level
```

## 🛠️ Code

```python
# serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 chars")
        return value

# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

## 🧪 Practice

1. Create a `PostSerializer` with fields `['id', 'title', 'content', 'author', 'is_published']`
2. Add validation: title must be at least 5 chars, content required
3. Serialize a single post and print `.data`
4. Deserialize invalid JSON (missing title) — check `.errors`
5. Use `many=True` to serialize a queryset
6. Add a `SerializerMethodField` called `comment_count`

## 🧠 Key Takeaways

- `ModelSerializer` infers fields from the model — less boilerplate
- `.is_valid()` triggers validation; `.errors` has error dicts
- `.save()` creates/updates instances from validated data
- `many=True` serializes multiple objects
- `read_only_fields` prevents client from setting server-controlled fields

"""DRF setup & serializers basics: ModelSerializer, validation, nested data."""
from typing import Any, Optional
from functools import wraps


# ======================== Data Store ========================
USERS: dict[int, dict] = {}
POSTS: list[dict] = []
PK = {"user": 1, "post": 1}


class User:
    def __init__(self, username: str, email: str):
        self.id = PK["user"]
        self.username = username
        self.email = email
        USERS[PK["user"]] = self
        PK["user"] += 1


class Post:
    def __init__(self, title: str, content: str, author_id: int):
        self.id = PK["post"]
        self.title = title
        self.content = content
        self.author_id = author_id
        POSTS.append(self)
        PK["post"] += 1


alice = User("alice", "alice@example.com")
bob = User("bob", "bob@example.com")
Post("Hello Django", "Content", alice.id)
Post("DRF Guide", "REST content", alice.id)
Post("Python Tips", "Tips content", bob.id)


# ======================== Serializer ========================
class Serializer:
    """Simulates DRF's Serializer with field validation and data conversion."""
    _fields: dict = {}

    def __init__(self, instance=None, data=None):
        self.instance = instance
        self.data_in = data or {}
        self._validated_data = {}
        self._errors = {}
        self._parsed_data = None

    def to_representation(self, instance) -> dict:
        raise NotImplementedError

    def to_internal_value(self, data: dict) -> dict:
        raise NotImplementedError

    def is_valid(self) -> bool:
        try:
            self._validated_data = self.to_internal_value(self.data_in)
            self._errors = {}
            return True
        except ValueError as e:
            self._errors = {"error": str(e)}
            return False

    @property
    def validated_data(self) -> dict:
        return self._validated_data

    @property
    def errors(self) -> dict:
        return self._errors

    @property
    def data(self):
        if self._parsed_data:
            return self._parsed_data
        if self.instance is not None:
            return self.to_representation(self.instance)
        return self._validated_data


# ======================== ModelSerializer ========================
class ModelSerializer(Serializer):
    """Simulates DRF's ModelSerializer with automatic field mapping."""
    class Meta:
        model = None
        fields = "__all__"
        read_only_fields = []

    def __init__(self, instance=None, data=None, many=False):
        self.many = many
        if many and data is not None:
            self._many_data = [ModelSerializer(instance=None, data=d) for d in data]
        super().__init__(instance, data)

    def get_fields(self) -> dict:
        """Infer field types from the model (simplified)."""
        return getattr(self.Meta, "fields", "__all__")

    @classmethod
    def _field_names(cls):
        meta = getattr(cls, "Meta", None)
        if not meta or not hasattr(meta, "model"):
            return []
        model = meta.model
        if not hasattr(model, "_fields"):
            return []
        return model._fields

    def to_representation(self, instance) -> dict:
        fields = self._field_names()
        read_only = getattr(self.Meta, "read_only_fields", [])
        result = {}
        for f in fields:
            val = getattr(instance, f, None)
            if f == "id":
                val = instance.id
            elif f.endswith("_id"):
                ref = getattr(instance, f.replace("_id", ""), None)
                if ref:
                    val = ref.id if hasattr(ref, "id") else ref
                    result[f.replace("_id", "")] = {"id": val}
            result[f] = val
        if read_only:
            for f in read_only:
                result[f] = getattr(instance, f, None)
        return result

    def to_internal_value(self, data: dict) -> dict:
        validated = {}
        fields = self._field_names()
        for f in fields:
            if f in data:
                validated[f] = data[f]
        if "title" in validated and len(validated["title"]) < 3:
            raise ValueError("Title must be at least 3 characters")
        return validated

    def is_valid(self) -> bool:
        if self.many:
            all_valid = all(s.is_valid() for s in self._many_data)
            if all_valid:
                self._validated_data = [s.validated_data for s in self._many_data]
            else:
                self._errors = [s.errors for s in self._many_data]
            return all_valid
        return super().is_valid()

    def save(self) -> Any:
        if self.instance:
            for k, v in self.validated_data.items():
                setattr(self.instance, k, v)
            return self.instance
        if self.Meta and self.Meta.model:
            return self.Meta.model(**self.validated_data)
        return self.validated_data


# ======================== Post Serializer ========================
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "author_id"]
        read_only_fields = ["id"]


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "author_id"]


# ======================== Demo ========================
print("=== DRF Serializers Demo ===")

# Serialize a single post
post = POSTS[0]
ser = PostSerializer(instance=post)
print(f"Serialized: {ser.data}")

# Serialize with author name resolved
post_data = ser.data
author = USERS.get(post.author_id)
post_data["author_name"] = author.username if author else "?"
print(f"With author: {post_data}")

# Deserialize (validation)
ser2 = PostSerializer(data={"title": "New Post", "content": "Great content", "author_id": 1})
print(f"\nDeserialize valid: {ser2.is_valid()}, data={ser2.validated_data}")

ser3 = PostSerializer(data={"title": "AB", "content": "Short title"})
print(f"Deserialize invalid: {ser3.is_valid()}, errors={ser3.errors}")

# Many = True (list serialization)
posts = POSTS
ser4 = PostSerializer(instance=posts, many=True)
print(f"\nMany serialized: {len(ser4.data)} posts")

# JSON rendering simulation
import json
print(f"\nJSON output: {json.dumps(ser.data, indent=2)}")

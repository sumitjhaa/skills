"""Advanced testing: factories, mocking, coverage, TDD patterns."""
from typing import Any, Optional, Callable
from functools import wraps
import json


# ======================== Simple Test Framework ========================

class TestCase:
    """Simulates Django's TestCase with assertions."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors: list[str] = []

    def assert_equal(self, a, b, msg=""):
        if a != b:
            self.fail(f"Expected {b!r}, got {a!r}. {msg}")

    def assert_true(self, expr, msg=""):
        if not expr:
            self.fail(f"Expected True, got {expr!r}. {msg}")

    def assert_false(self, expr, msg=""):
        if expr:
            self.fail(f"Expected False, got {expr!r}. {msg}")

    def assert_in(self, item, container, msg=""):
        if item not in container:
            self.fail(f"Expected {item!r} in {container!r}. {msg}")

    def assert_raises(self, exc_class, callable_obj, *args, **kwargs):
        try:
            callable_obj(*args, **kwargs)
            self.fail(f"Expected {exc_class.__name__} but no exception raised")
        except exc_class:
            pass
        except Exception as e:
            self.fail(f"Expected {exc_class.__name__} but got {type(e).__name__}: {e}")

    def fail(self, msg=""):
        self.failed += 1
        self.errors.append(msg)

    def run(self, test_methods: list[str] = None):
        """Discover and run test methods."""
        methods = test_methods or [m for m in dir(self) if m.startswith("test_")]
        for method_name in methods:
            method = getattr(self, method_name)
            try:
                self.setUp()
                method()
                self.passed += 1
                print(f"  ✅ {method_name}")
            except AssertionError as e:
                self.failed += 1
                self.errors.append(str(e))
                print(f"  ❌ {method_name}: {e}")
            except Exception as e:
                self.failed += 1
                self.errors.append(str(e))
                print(f"  💥 {method_name}: {type(e).__name__}: {e}")

    def setUp(self):
        """Override for test setup."""
        pass

    def tearDown(self):
        """Override for test cleanup."""
        pass

    def summary(self):
        total = self.passed + self.failed
        print(f"\n   {'='*40}")
        print(f"   {total} tests: {self.passed} passed, {self.failed} failed")
        if self.errors:
            for err in self.errors[:3]:
                print(f"   ! {err}")
        return self.failed == 0


# ======================== Mocking ========================

class Mock:
    """Simple mock object for testing."""
    def __init__(self, **attrs):
        self._calls: list[tuple] = []
        for k, v in attrs.items():
            setattr(self, k, v)

    def __call__(self, *args, **kwargs):
        self._calls.append(("__call__", args, kwargs))
        if hasattr(self, "return_value"):
            return self.return_value
        return None

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        return MockMethod(name, self)

    def assert_called_once(self):
        assert len(self._calls) == 1, f"Expected 1 call, got {len(self._calls)}"

    def assert_called_with(self, *args, **kwargs):
        if self._calls:
            last_call = self._calls[-1]
            assert last_call[1:] == (args, kwargs), f"Expected call {args, kwargs}, got {last_call[1:]}"


class MockMethod:
    """Mock method that records calls."""
    def __init__(self, name: str, parent: Mock):
        self.name = name
        self.parent = parent

    def __call__(self, *args, **kwargs):
        self.parent._calls.append((self.name, args, kwargs))
        if hasattr(self.parent, f"{self.name}_return"):
            return getattr(self.parent, f"{self.name}_return")
        return None


# ======================== Factory Boy Simulation ========================

class Factory:
    """Simulates factory_boy for test data generation."""
    model = None
    defaults: dict = {}

    @classmethod
    def build(cls, **overrides) -> dict:
        """Build a dict without saving."""
        data = dict(cls.defaults)
        data.update(overrides)
        return data

    @classmethod
    def create(cls, **overrides) -> dict:
        """Create and return a dict (simulated DB save)."""
        obj = cls.build(**overrides)
        obj['id'] = hash(str(obj)) % 100000
        return obj

    @classmethod
    def build_batch(cls, count: int, **overrides) -> list[dict]:
        return [cls.build(**overrides) for _ in range(count)]

    @classmethod
    def create_batch(cls, count: int, **overrides) -> list[dict]:
        return [cls.create(**overrides) for _ in range(count)]


class PostFactory(Factory):
    model = "Post"
    defaults = {
        "title": "Test Post",
        "content": "Test content for testing",
        "author": "alice",
        "is_published": True,
    }


class CommentFactory(Factory):
    model = "Comment"
    defaults = {
        "text": "Great post!",
        "author": "bob",
        "post_id": 1,
    }


# ======================== Code Under Test ========================

def calculate_post_stats(posts: list[dict]) -> dict:
    """Calculate some statistics from a list of posts."""
    if not posts:
        return {"total": 0, "published": 0, "avg_likes": 0}

    published = [p for p in posts if p.get("is_published")]
    total_likes = sum(p.get("likes", 0) for p in posts)
    return {
        "total": len(posts),
        "published": len(published),
        "avg_likes": round(total_likes / len(posts), 1),
    }


def validate_post_data(data: dict) -> list[str]:
    """Validate post creation data. Returns list of errors (empty = valid)."""
    errors = []
    if not data.get("title"):
        errors.append("Title is required")
    elif len(data["title"]) < 3:
        errors.append("Title must be at least 3 characters")
    if not data.get("content"):
        errors.append("Content is required")
    if data.get("is_published") and not data.get("author"):
        errors.append("Author required for published posts")
    return errors


# ======================== Tests ========================

class TestPostStats(TestCase):
    def test_empty_posts(self):
        result = calculate_post_stats([])
        self.assert_equal(result["total"], 0)
        self.assert_equal(result["published"], 0)

    def test_all_published(self):
        posts = PostFactory.create_batch(3, is_published=True, likes=10)
        result = calculate_post_stats(posts)
        self.assert_equal(result["total"], 3)
        self.assert_equal(result["published"], 3)

    def test_mixed_published(self):
        posts = [
            PostFactory.create(is_published=True, likes=10),
            PostFactory.create(is_published=False, likes=5),
        ]
        result = calculate_post_stats(posts)
        self.assert_equal(result["published"], 1)
        self.assert_equal(result["total"], 2)

    def test_avg_likes(self):
        posts = [
            PostFactory.create(likes=10),
            PostFactory.create(likes=20),
        ]
        result = calculate_post_stats(posts)
        self.assert_equal(result["avg_likes"], 15.0)


class TestPostValidation(TestCase):
    def test_valid_post(self):
        data = {"title": "Hello", "content": "World", "author": "alice", "is_published": True}
        errors = validate_post_data(data)
        self.assert_equal(len(errors), 0)

    def test_missing_title(self):
        data = {"content": "World"}
        errors = validate_post_data(data)
        self.assert_in("Title is required", errors)

    def test_short_title(self):
        data = {"title": "AB", "content": "World"}
        errors = validate_post_data(data)
        self.assert_in("Title must be at least 3 characters", errors)

    def test_missing_content(self):
        errors = validate_post_data({"title": "Hello"})
        self.assert_in("Content is required", errors)

    def test_published_no_author(self):
        data = {"title": "Hello", "content": "World", "is_published": True}
        errors = validate_post_data(data)
        self.assert_in("Author required for published posts", errors)


class TestFactory(TestCase):
    def test_factory_build(self):
        post = PostFactory.build(title="Custom Title")
        self.assert_equal(post["title"], "Custom Title")
        self.assert_equal(post["author"], "alice")  # from defaults

    def test_factory_create(self):
        post = PostFactory.create()
        self.assert_true("id" in post)

    def test_factory_batch(self):
        posts = PostFactory.create_batch(5)
        self.assert_equal(len(posts), 5)

    def test_factory_overrides(self):
        posts = CommentFactory.create_batch(3, post_id=5)
        for p in posts:
            self.assert_equal(p["post_id"], 5)


class TestMocking(TestCase):
    def test_mock_call(self):
        m = Mock(return_value=42)
        result = m(1, 2, key="val")
        self.assert_equal(result, 42)
        m.assert_called_once()

    def test_mock_method(self):
        m = Mock()
        m.get_user_return = {"name": "Alice"}
        result = m.get_user(1)
        self.assert_equal(result, {"name": "Alice"})
        self.assert_equal(len(m._calls), 1)


# ======================== Demo ========================
print("=== Advanced Testing Demo ===\n")

# Run tests
test_classes = [TestPostStats, TestPostValidation, TestFactory, TestMocking]
all_passed = True

for test_cls in test_classes:
    test_name = test_cls.__name__
    print(f"\n{test_name}:")
    suite = test_cls()
    suite.run()
    if not suite.summary():
        all_passed = False

print(f"\n{'='*40}")
print(f"Overall: {'✅ All tests passed' if all_passed else '❌ Some tests failed'}")

# --- Coverage concept ---
print("\n--- Coverage Summary (conceptual) ---")
print("  Statements: 45/50 covered (90%)")
print("  Branches:   12/14 covered (86%)")
print("  Functions:  6/6 covered (100%)")

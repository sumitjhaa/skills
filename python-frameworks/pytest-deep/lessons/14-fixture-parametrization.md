# 🔄 Fixture Parametrization
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Parametrize fixtures with `params`, `indirect` parametrization, fixture factories.

## Fixture with params

```python
@pytest.fixture(params=["sqlite", "postgresql"])
def db(request):
    if request.param == "sqlite":
        return create_engine("sqlite:///:memory:")
    else:
        return create_engine("postgresql://localhost/test")

# Each test runs twice — once per param
```

## Indirect Parametrization

```python
@pytest.fixture
def user(request):
    return create_user(role=request.param)

@pytest.mark.parametrize("user", ["admin", "user"], indirect=True)
def test_access(user):
    assert user.role in ("admin", "user")
```

## Factory as Fixture

```python
@pytest.fixture
def make_user():
    created = []
    
    def _make(name, role="user"):
        u = User(name=name, role=role)
        created.append(u)
        return u
    
    yield _make
    
    # Cleanup
    for u in created:
        u.delete()

def test_multiple(make_user):
    alice = make_user("Alice", "admin")
    bob = make_user("Bob")
    assert alice.role == "admin"
```

## Dynamic Fixture Values

```python
@pytest.fixture
def config(request):
    """Return different configs based on marker."""
    if request.node.get_closest_marker("slow"):
        return {"timeout": 60}
    return {"timeout": 5}
```

<!-- 🧠 `request.param` and `request.node` give access to the requesting test context. -->

## Run the Code

```bash
pytest code/14-fixture-parametrization.py -v
```

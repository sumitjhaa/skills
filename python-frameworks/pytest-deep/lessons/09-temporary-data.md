# 📂 Temporary Data
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** tmp_path, tmp_path_factory, tmpdir for filesystem tests.

## tmp_path (pathlib.Path)

```python
def test_create_file(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    f = d / "test.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"
    assert f.stat().st_size == 5
```

## tmp_path_factory (Session-Scoped)

```python
@pytest.fixture(scope="session")
def shared_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("shared")

def test_one(shared_dir):
    (shared_dir / "file.txt").write_text("data")
```

## tmpdir (Legacy, py.path)

```python
def test_old_style(tmpdir):
    f = tmpdir.join("test.txt")
    f.write("hello")
    assert f.read() == "hello"
```

## Unique Directories

Each test gets a unique temporary directory — no collision between tests.

```python
def test_a(tmp_path):
    # /tmp/pytest-0/test_a0/
    ...

def test_b(tmp_path):
    # /tmp/pytest-0/test_b1/
    ...
```

## Cleaning Up

Pytest removes `tmp_path` after each test by default. Keep with:

```bash
pytest --basetemp=/tmp/my-tests
```

<!-- 🤔 Prefer `tmp_path` (pathlib) over `tmpdir` (py.path) for new code. -->

## Run the Code

```bash
pytest code/09-temporary-data.py -v
```

"""Temporary data — tmp_path, tmp_path_factory."""
import pytest


def test_tmp_path(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    f = d / "test.txt"
    f.write_text("Hello, pytest!")
    assert f.read_text() == "Hello, pytest!"
    assert f.exists()


def test_multiple_files(tmp_path):
    for i in range(3):
        f = tmp_path / f"file_{i}.txt"
        f.write_text(str(i))
    files = list(tmp_path.iterdir())
    assert len(files) == 3


def test_nested_dirs(tmp_path):
    path = tmp_path / "a" / "b" / "c"
    path.mkdir(parents=True)
    assert path.exists()
    assert path.is_dir()


def test_binary_file(tmp_path):
    data = bytes(range(256))
    f = tmp_path / "data.bin"
    f.write_bytes(data)
    assert f.read_bytes() == data


def test_json_file(tmp_path):
    import json
    data = {"name": "Alice", "scores": [1, 2, 3]}
    f = tmp_path / "data.json"
    f.write_text(json.dumps(data))
    loaded = json.loads(f.read_text())
    assert loaded == data


@pytest.fixture(scope="session")
def shared_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("shared")


def test_shared_dir(shared_dir):
    f = shared_dir / "shared.txt"
    f.write_text("shared data")
    assert f.exists()


def test_shared_clean(tmp_path_factory):
    """Each call to mktemp gives a unique dir."""
    d1 = tmp_path_factory.mktemp("unique")
    d2 = tmp_path_factory.mktemp("unique")
    assert d1 != d2

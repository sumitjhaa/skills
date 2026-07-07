"""Tests using shared fixtures from conftest.py."""
def test_db_set_get(db):
    db.set("name", "Alice")
    assert db.get("name") == "Alice"


def test_db_clear(db):
    db.set("key", "value")
    db.clear()
    assert db.get("key") is None


def test_sample_user(sample_user):
    assert sample_user["name"] == "Alice"
    assert sample_user["email"] == "alice@test.com"


def test_fixture_combination(db, sample_user):
    db.set("user", sample_user)
    retrieved = db.get("user")
    assert retrieved["id"] == 1
    assert retrieved["name"] == "Alice"

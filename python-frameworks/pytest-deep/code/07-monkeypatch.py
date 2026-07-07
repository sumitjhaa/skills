"""Monkeypatch — replace env vars, attributes, and functions."""
import pytest
import os
import sys


API_URL = "https://api.example.com"
DEBUG = True


def load_config():
    return {
        "database_url": os.environ.get("DATABASE_URL", "sqlite:///dev.db"),
        "debug": DEBUG,
    }


def test_set_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    assert os.environ["DATABASE_URL"] == "sqlite:///test.db"


def test_delete_env(monkeypatch):
    monkeypatch.setenv("TEMP_KEY", "value")
    monkeypatch.delenv("TEMP_KEY", raising=False)
    assert "TEMP_KEY" not in os.environ


def test_set_attribute(monkeypatch):
    this_module = sys.modules[__name__]
    monkeypatch.setattr(this_module, "DEBUG", False)
    config = load_config()
    assert config["debug"] is False


def test_set_env_restored(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql:///test")
    config = load_config()
    assert "postgresql" in config["database_url"]


def test_dict(monkeypatch):
    data = {"key": "original"}
    monkeypatch.setitem(data, "key", "modified")
    assert data["key"] == "modified"

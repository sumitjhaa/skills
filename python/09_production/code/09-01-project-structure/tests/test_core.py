"""Tests for my_project.core."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from my_project.core import greet


def test_greet():
    assert greet("Alice") == "Hello, Alice!"


def test_greet_empty():
    assert greet("") == "Hello, !"

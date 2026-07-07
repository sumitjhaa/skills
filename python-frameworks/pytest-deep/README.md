# 🧪 pytest Deep-Dive

pytest is Python's most popular testing framework. Simple assertions, powerful fixtures, rich plugin ecosystem.

## Structure

```
pytest-deep/
├── lessons/      # 15 markdown lessons
├── code/         # 15 runnable test files
├── practice/     # 1 exercise set
└── README.md     # this file
```

## Lessons

| # | Lesson | Code | What You'll Learn |
|---|--------|------|-------------------|
| 01 | Getting Started | ✅ | Assertions, test discovery, running tests |
| 02 | Fixtures Basics | ✅ | Dependency injection, yield, autouse |
| 03 | Fixture Scopes | ✅ | function/module/session scopes |
| 04 | Parametrize | ✅ | Multiple inputs, stacking, test IDs |
| 05 | Marks | ✅ | skip, xfail, custom marks |
| 06 | Conftest | ✅ | Shared fixtures, hierarchy |
| 07 | Monkeypatch | ✅ | Env vars, attributes, functions |
| 08 | Mocking | ✅ | pytest-mock, call assertions, side effects |
| 09 | Temporary Data | ✅ | tmp_path, tmp_path_factory |
| 10 | Exceptions & Warnings | ✅ | raises, warns |
| 11 | Approx Comparisons | ✅ | Float tolerance, approx |
| 12 | Configuration | ✅ | pytest.ini, pyproject.toml, CLI flags |
| 13 | Doctests | ✅ | Docstring examples |
| 14 | Fixture Parametrization | ✅ | params, indirect, factories |
| 15 | Integration | ✅ | Full task manager test suite |

## Quick Start

```bash
pip install pytest pytest-mock
pytest code/01-getting-started.py -v
```

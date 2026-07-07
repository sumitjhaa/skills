# ✅ Pydantic Deep-Dive

Pydantic is Python's most popular data validation library. Used everywhere — FastAPI, SQLModel, LangChain, and more.

## Structure

```
pydantic/
├── lessons/      # 10 markdown lessons
├── code/         # 10 runnable Python files
├── practice/     # 1 exercise set
└── README.md     # this file
```

## Lessons

| # | Lesson | Code | What You'll Learn |
|---|--------|------|-------------------|
| 01 | Basics | ✅ | `BaseModel`, validation, `model_dump` |
| 02 | Field Types | ✅ | Constraints, defaults, optional fields |
| 03 | Nested Models | ✅ | Embedding, lists, recursion |
| 04 | Validators | ✅ | Field validators, model validators |
| 05 | Serialization | ✅ | `model_dump_json`, include/exclude, aliases |
| 06 | Model Config | ✅ | Frozen, extra, populate_by_name |
| 07 | Strict Mode | ✅ | Type coercion, `Strict*` types |
| 08 | Custom Types | ✅ | `TypeAdapter`, generics, custom validators |
| 09 | Error Handling | ✅ | `ValidationError`, error inspection |
| 10 | Integration | ✅ | Settings, API schemas, full pipeline |

## Quick Start

```bash
pip install pydantic pydantic-settings
python code/01-basics.py
```

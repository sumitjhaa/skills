# 🏁 Integration: Blog API
<!-- ⏱️ 20 min | 🟢 Challenge -->

**What You'll Learn:** Combine everything from Phase 01 into a working Blog API with CRUD, validation, errors, and docs.

## Features

- Full CRUD for posts CRUD for posts
- Pydantic validation
- Error handling with proper status codes
- In-memory database (swappable to real DB later)
- Auto-generated OpenAPI docs

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/posts` | List all posts (with pagination) |
| `GET` | `/posts/{id}` | Get single post |
| `POST` | `/posts` | Create post |
| `PUT` | `/posts/{id}` | Update post |
| `DELETE` | `/posts/{id}` | Delete post |
| `GET` | `/health` | Health check |

## Models

```python
class Post(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=10)
    published: bool = True

class PostOut(Post):
    id: int
    created_at: datetime
```

<!-- 🗺️ This structure maps directly to a real database model. Migrate from dict → SQLite → PostgreSQL seamlessly. -->

## Key Patterns Used

| Pattern | Where |
|---------|-------|
| Path params | `GET /posts/{id}` |
| Query params | Pagination `offset`/`limit` |
| Request body | `POST` / `PUT` payloads |
| Response model | `PostOut` hides internal fields |
| Status codes | `201` for create, `204` for delete |
| HTTPException | `404` when post not found |

## Running

```bash
python code/10-integration-blog-api.py
```

<!-- 🎯 This is the blueprint for every future Phase 01 integration project. Master it. -->

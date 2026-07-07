# 🏋️ FastAPI Practice — Phase 01

## 1. 🟢 Project Setup
Create a FastAPI project called `library_api`. Add endpoints: `GET /` (welcome message), `GET /health` (status + version). Run with Uvicorn. Verify `/docs` renders.

## 2. 🟢 Path & Query Params
Add endpoints: `GET /books/{book_id}` (path param, int), `GET /books` (query params: `author`, `year`, `limit=10`). Validate types.

## 3. 🟡 Pydantic Models
Define `Book` model: `title` (min_length=1, max_length=200), `author` (min_length=3), `year` (ge=1900, le=2030), `rating` (ge=0.0, le=10.0, default=0.0), `in_stock` (bool, default=True). Test with valid and invalid input.

## 4. 🟡 Response Models
Create `BookOut` that excludes `in_stock`. Create `POST /books` with `response_model=BookOut` and `status_code=201`. Verify the response omits `in_stock`.

## 5. 🟡 Error Handling
Add `GET /books/{book_id}` that raises `HTTPException(404)` for unknown IDs. Add a custom exception handler for `ValueError` that returns `400`.

## 6. 🟡 Dependencies
Create a `Pagination` dependency (`offset`, `limit` with defaults). Use it in `GET /books` for paginated listing.

## 7. 🟢 CORS
Add CORS middleware allowing `http://localhost:5173` (Vite dev server). Verify headers with `curl -I`.

## 8. 🟡 Routers
Refactor into `routers/books.py` and `routers/authors.py` using `APIRouter` with prefix and tags. Include in `main.py`.

## 9. 🟢 Static & Templates
Add a `GET /about` endpoint that renders an HTML template with app info. Mount a `static/` directory with a CSS file.

## 10. 🔴 Complete Library API
Build a full CRUD Library API with:
- `Author` model (name, bio, birth_year)
- `Book` model (title, author_id, year, rating, in_stock)
- All CRUD endpoints for both models
- Pagination, validation, error handling
- Response models for create vs list vs detail
- Routers in separate files
- CORS configured
- Auto-generated docs at `/docs`

# 🏋️ Flask Practice — Phase 01

## 1. 🟢 Project Setup
Create a Flask project called `portfolio`. Add endpoints: `GET /` (welcome), `GET /about` (bio + skills list), `GET /contact` (contact info). Run with `flask run --debug`.

## 2. 🟢 Templates
Create a base template (`base.html`) with nav, content block, and footer. Create child templates for home, about, and contact pages. Pass dynamic data (title, year, page-specific content) from routes.

## 3. 🟢 Static Files
Add `css/style.css` (styling for nav, body, footer) and `js/script.js` (console greeting). Link them in templates using `url_for('static', ...)`. Add a dark mode stylesheet toggle.

## 4. 🟡 Request Handling
Create `GET /search` accepting `q`, `category`, `page`, `limit` query params. Create `POST /feedback` accepting `name`, `email`, `rating`, `message` with server-side validation. Return appropriate error messages.

## 5. 🟡 WTForms
Define `ProductForm` with fields: `name` (required, 3-100 chars), `price` (required, float), `category` (select: electronics/books/clothing), `in_stock` (boolean). Create `GET` and `POST` handler that validates and returns form data or errors.

## 6. 🟡 SQLAlchemy Models
Define `Author` (name, bio, birth_year) and `Book` (title, author_id, year, genre, rating) models. Create endpoints: list all books, get by ID, filter by genre, create book, get author's books. Use proper relationships.

## 7. 🟡 Blueprints
Refactor your portfolio into blueprints: `main_bp` (home, about, contact), `blog_bp` (post listing, detail), `admin_bp` (dashboard, settings). Register all with appropriate URL prefixes. Verify all routes work.

## 8. 🟢 Error Handling
Add custom error handlers for 404 (friendly "page not found" message), 403 ("access denied" with suggestions), and 500 (generic error with reference ID). Test by triggering each error type.

## 9. 🟡 Sessions & Flash
Build a simple note-taking app: login stores username in session, add notes (stored in session list), view notes, delete notes, logout. Use flash messages for all operations. Session persists note list across requests.

## 10. 🔴 Complete Blog App
Build a full Flask blog with:
- User registration, login, logout (session-based)
- Create, view, edit, delete posts (own posts only)
- Comments on posts (auth required)
- Flash messages for all actions
- Jinja2 templates with inheritance
- Static CSS styling
- Error handling (404, 403, 500)
- Post listing with comment counts
- Blog blueprint structure

# 🐍 Python Full-Stack — Baby Style (8 weeks)

**For:** Know nothing. Want Python. Need small steps.

**Time:** 3-4 hrs/day | **Goal:** Junior Python web developer

---

## 🗓️ Week 1 — Python (just enough)

### Day 1: Variables + Print
- `name = "Alex"` — stores text
- `age = 25` — stores number
- `print(name)` — shows it

**Do:** Make 3 variables. Print them. Run the file.

### Day 2: Functions
- `def double(n): return n * 2` — takes input, gives output
- `double(5)` → 10

**Do:** Write a function that greets a person. `greet("Alex")` → "Hello Alex"

### Day 3: Lists + Loops
- `colors = ["red", "blue", "green"]` — list of things
- `colors[0]` = "red" (starts at 0)
- `for c in colors: print(c)` — go through each

**Do:** Make a list of 3 foods. Loop through and print each.

### Day 4: If/else + Input
- `if x > 10: print("big")` else: print("small")
- `name = input("Your name: ")` — ask user

**Do:** Ask user age. Print "adult" if 18+, "kid" if less.

### Day 5: Dictionaries
- `person = {"name": "Alex", "age": 25}` — like object in JS
- `person["name"]` → "Alex"

**Do:** Make a dict for a movie (title, year, rating). Print each.

### Day 6-7: Mini project
**Do:** Command line todo list:
- Show list of todos
- Add todo (input)
- Done todo (remove)
- Run in terminal

---

## 🗓️ Week 2 — Python Web (FastAPI)

### Day 1: What is FastAPI?
- Makes web servers in Python. Fast. Simple.
- Auto generates docs (Swagger UI)

**Do:** Install FastAPI + uvicorn. Run the "Hello World" example from their docs.

### Day 2: Routes
- `@app.get("/")` — handles GET requests
- `@app.post("/items")` — handles POST

**Do:** Make 3 routes: / (hello), /about (about page), /api/data (JSON).

### Day 3-4: Pydantic (data validation)
- `class Item(BaseModel): name: str; price: float`
- FastAPI checks types automatically

**Do:** Make a model for Todo (id, title, done). Create POST route for it.

### Day 5-6: SQL + PostgreSQL
- PostgreSQL = database (stores data permanently)
- SQL: `SELECT * FROM todos`, `INSERT INTO todos ...`

**Do:** Install PostgreSQL. Create a table. Insert 3 rows. Select them.

### Day 7: SQLAlchemy (talk to DB from Python)
- SQLAlchemy = write SQL in Python
- `session.query(Todo).all()` — get all todos

**Do:** Connect FastAPI to PostgreSQL via SQLAlchemy. GET /todos returns DB data.

---

## 🗓️ Week 3 — React (frontend for your Python backend)

### Day 1: What is React?
- Makes websites. Components = LEGO blocks.

**Do:** `npx create-react-app my-app` then `npm start`. See the page.

### Day 2: JSX + Props
- `function Hello() { return <h1>Hi</h1>; }`
- Props = inputs: `<Hello name="Alex" />`

**Do:** Make a `Card` component. Use it 3 times.

### Day 3: State (useState)
- `const [count, setCount] = useState(0)`
- `setCount(count + 1)` — updates

**Do:** Build a counter. +1, -1, reset buttons.

### Day 4: Fetching data
- `fetch("http://localhost:8000/todos")` — call your Python API
- Show results on page

**Do:** Display your todos from the FastAPI server.

### Day 5: Forms + POST
- Form → input → submit → send POST to your API

**Do:** Add form to create new todo. Send to backend. Refresh list.

### Day 6-7: Router + Polish
- React Router: multiple pages
- Clean up styles (Tailwind CSS)

**Do:** 3 pages: Home (todo list), About, Contact. Wire up all CRUD.

---

## 🗓️ Week 4 — Django (Python's main web framework)

### Day 1: What is Django?
- Django = "batteries included" — has everything built in
- Admin panel, auth, ORM, forms — all included

**Do:** Install Django. `django-admin startproject mysite`. See it run.

### Day 2: Django apps + views
- Project = website. App = feature (blog, shop, etc.)
- View = function that handles a URL

**Do:** Create a "todos" app. Make a view that returns "Hello".

### Day 3: Django ORM + Models
- Models = database tables in Python
- `class Todo(models.Model): title = models.CharField(...)`

**Do:** Make a Todo model. Run migrations. Add some via admin panel.

### Day 4: Django Admin
- Admin panel = FREE UI for your data (generated automatically)
- Go to `/admin`. See your todos. Add/edit/delete.

**Do:** Customize admin to show all todo fields nicely.

### Day 5: Templates
- Django shows HTML via templates
- `return render(request, "list.html", {"todos": todos})`

**Do:** Show your todos in a HTML page with nice styling.

### Day 6-7: Django REST Framework (DRF)
- DRF = makes JSON APIs with Django
- Serializers = convert models to JSON

**Do:** Build a REST API for todos using DRF. Test with Postman.

---

## 🗓️ Week 5 — Full-stack Django + React OR HTMX

### Option A: Django + React
- Backend: Django + DRF (your API)
- Frontend: React (fetches from your API)

**Do:** Connect your React app (from week 3) to your Django API.

### Option B: Django + HTMX (easier, one language)
- HTMX = add dynamic behavior to HTML without React
- `hx-post="/todos"` — sends request, updates page
- One language: Python + HTML. No JSON API needed.

**Do:** Build a todo list with Django + HTMX. Add, delete, toggle done — all without page reload.

### Day 1-2: Auth (Django built-in)
- Django has login/signup built in
- `python manage.py createsuperuser`

**Do:** Add login page. Only logged-in users can see todos.

### Day 3-5: Build the app
```
- User signup/login
- Each user has their own todos
- Create, read, update, delete todos
- Mark done / not done
```

### Day 6-7: Deploy
- Deploy Django to Render or Railway (free)
- Deploy React to Vercel (free)
- Or deploy Django + HTMX all in one place

---

## 🗓️ Week 6 — Big Project (pick one)

**Project A: Blog**
```
- Users: signup, login, profiles
- Posts: create, edit, delete
- Comments on posts
- Django admin for moderation
```

**Project B: Inventory tracker**
```
- Add items (name, quantity, price)
- Search/filter items
- Low stock alerts
- Export to CSV
```

**Project C: Habit tracker**
```
- Add habits (drink water, exercise)
- Check off daily
- Show streak (days in a row)
- Dashboard with progress
```

---

## 🗓️ Week 7 — Resume + Apply

### Day 1: Resume
- 1 page. Projects as experience.
- Keywords: Python, Django, FastAPI, PostgreSQL, React, REST APIs

### Day 2: LinkedIn
- Photo. Headline: "Junior Python Developer"
- Add projects with screenshots

### Day 3-4: LeetCode (in Python)
- 3 easy problems/day (arrays, strings, loops)
- Python is great for interviews (short syntax)

### Day 5-6: Apply
- LinkedIn Jobs → "Junior Python Developer", "Django Developer"
- Indeed, pythonjobs.com, djangojobs.com
- 10 apps/day

### Day 7: Follow up
- Message recruiters on LinkedIn
- Join Python Discord, Django forums

---

## 🗓️ Week 8 — Keep applying

- 10 apps/day
- 2 LeetCode problems/day
- Review projects (can you explain every line?)
- Practice "tell me about yourself" (30 sec)

---

> ✅ **Python is versatile.** After you get a job, you can pivot to data engineering, DevOps, or ML later — all higher paying.

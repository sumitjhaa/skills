# 🏃 JS/TS Full-Stack — Baby Style (8 weeks)

**For:** Know nothing. Want job fast. Need small steps.

**Time:** 3-4 hrs/day | **Goal:** Junior web developer

---

## 🗓️ Week 1 — JavaScript (just enough)

### Day 1: Variables
- `let name = "Alex"` — stores text
- `let age = 25` — stores number
- `console.log(name)` — shows it in console (F12 → Console)

**Do:** Make 3 variables. Log them. See them appear.

### Day 2: Functions
- `function double(n) { return n * 2; }` — takes input, returns output
- `double(5)` → 10

**Do:** Write a function that adds 2 numbers. Test it.

### Day 3: Arrays + Loops
- `let list = ["a", "b", "c"]` — list of things
- `list[0]` = "a" (starts at 0)
- `for (let item of list) { console.log(item); }` — go through each

**Do:** Make a list of 3 colors. Loop through and log each.

### Day 4: If/else
- `if (x > 10) { console.log("big"); } else { console.log("small"); }`

**Do:** Write code that says "even" or "odd" for any number.

### Day 5: Objects
- `let person = { name: "Alex", age: 25 }`
- `person.name` → "Alex"

**Do:** Make a car object (brand, year, color). Log each property.

### Day 6-7: Mini project
**Do:** A page with:
- Button that shows "Hello" when clicked
- Counter that goes up/down
- Changes background color

---

## 🗓️ Week 2 — TypeScript (makes hiring easier)

### Day 1: What is TS?
- JS but with types: `let name: string = "Alex"`
- Prevents mistakes (can't put number in string box)

**Do:** Add `: number` and `: string` to your variables.

### Day 2-3: Interfaces
- `interface Person { name: string; age: number; }`
- Describes what an object should look like

**Do:** Make an interface for a Movie (title, year, rating). Create one.

### Day 4-5: REST APIs
- Websites talk to each other with HTTP (GET/POST/PUT/DELETE)
- GET = get data. POST = create. PUT = update. DELETE = remove.

**Do:** Use Postman to GET data from `https://api.github.com/users/defunkt`

### Day 6-7: Fetch data
- `fetch("https://api.github.com/users/yourname")`
- `await response.json()` — convert to usable data

**Do:** Fetch a GitHub user. Show name + avatar on a page.

---

## 🗓️ Week 3 — React (companies pay for this)

### Day 1: What is React?
- Makes building websites easier
- Components = reusable pieces (like LEGO blocks)

**Do:** `npx create-react-app my-app` then `npm start`. See the default page.

### Day 2: JSX + Props
- JSX = HTML in JS: `function Hello() { return <h1>Hi</h1>; }`
- Props = inputs: `<Hello name="Alex" />`

**Do:** Make a `Card` component. Use it 3 times with different data.

### Day 3: State (useState)
- `const [count, setCount] = useState(0)` — remembers values
- `setCount(count + 1)` — updates

**Do:** Build a counter (increment + decrement + reset).

### Day 4: Effect (useEffect)
- Runs code when page loads: `useEffect(() => { fetch(...) }, [])`

**Do:** Fetch GitHub user data when page loads. Show it.

### Day 5: Router
- React Router = multiple pages without reloading
- `<Route path="/" element={<Home />} />`

**Do:** Make 3 pages (Home, About, Projects). Navigate between them.

### Day 6-7: Build mini project
**Do:** A GitHub profile explorer:
- Search box → type username → see their repos
- Loading spinner while fetching
- Error if not found

---

## 🗓️ Week 4 — React deeper + Next.js

### Day 1-2: More practice
- Forms: input → store in state → display
- Conditional rendering: `{isLoading ? <Spinner /> : <Data />}`

**Do:** Add a simple form to your app (name + email inputs).

### Day 3-4: Next.js
- Next = React on steroids (pages, fast loading)
- Pages inside `pages/` folder = automatic routes
- Deploy to Vercel (free, 1 click)

**Do:** Rebuild your portfolio in Next.js. Deploy to Vercel.

### Day 5-7: Deploy everything
- Put all your projects on GitHub
- Deploy to Vercel or Netlify
- Write README for each (what, why, how, live link)

---

## 🗓️ Week 5 — Backend (Node.js + Database)

### Day 1: Node.js
- JS that runs on a server (not in browser)
- `node myfile.js` — runs the file

**Do:** Make a file that logs "Hello" and run it with Node.

### Day 2: Express
- Express = makes servers easy
- `app.get("/", (req, res) => res.send("Hello"))`

**Do:** Make a server with 3 routes (/, /about, /api/data). Test in browser.

### Day 3-4: Database (PostgreSQL + Prisma)
- PostgreSQL = stores data (like Excel but for code)
- Prisma = talk to database easily

**Do:** Install Prisma. Make schema for User + Todo. Run migration.

### Day 5: Connect DB to server
- Express route → query database → return JSON

**Do:** GET /todos returns all todos from DB. POST /todos adds one.

### Day 6-7: Auth (JWT)
- JWT = token that proves你是谁
- Signup: create user → return token
- Login: check password → return token

**Do:** Add signup + login to your server. Protect a route.

---

## 🗓️ Week 6 — Build your big project

Build a **Task Manager** (mini Trello):

```
Day 1: Backend setup (Express + Prisma + Postgres)
Day 2: User auth (signup + login + JWT)
Day 3: Project routes (create, list, delete projects)
Day 4: Task routes (create, move, delete tasks)
Day 5: Frontend login + dashboard
Day 6: Frontend project board with tasks
Day 7: Connect frontend → backend. Deploy both.
```

---

## 🗓️ Week 7 — Resume + Apply

### Day 1: Resume
- 1 page. Projects as experience.
- "Built a task manager with React + Node.js + PostgreSQL"

### Day 2: LinkedIn
- Photo. Headline: "Junior Web Developer"
- Add your projects with screenshots

### Day 3-4: LeetCode
- 3 easy problems (arrays, strings, loops)
- Do them in JavaScript

### Day 5-6: Apply
- LinkedIn Jobs → "Junior Developer", "Entry Level"
- Indeed → same
- 10 apps/day

### Day 7: Follow up
- Message recruiters on LinkedIn
- "Hi, I applied for X. Excited about your team."

---

## 🗓️ Week 8 — Keep applying

- 10 apps/day minimum
- 2 LeetCode problems/day
- Review your projects (can you explain every line?)
- Practice "tell me about yourself" (30 sec)

---

> ✅ **After 8 weeks:** 4 projects, 1 deployed app, 100+ applications. First job usually comes week 6-10 of searching.

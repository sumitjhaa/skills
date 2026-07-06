# 🧪 QA / Test Automation — Baby Style (4-5 weeks)

**For:** No coding experience. Want tech job fast. Don't want to build websites.

**Time:** 3 hrs/day | **Goal:** QA Tester / Test Automation Engineer

**Pay:** $50-75k | **Difficulty:** Easiest path into tech

---

## What is QA?

- QA = Quality Assurance = finding bugs in software
- You click around apps, find what's broken, report it
- Then you automate: write code that clicks for you
- Companies NEED testers. Entry level jobs exist.

---

## 🗓️ Week 1 — Manual Testing (no code)

### Day 1: What is testing?
- Developers write code. Testers break it.
- Bug = something that doesn't work right
- Test case = steps to check if something works

**Do:** Open any app. Try to break it. Click wrong buttons. Enter weird text. Note what happens.

### Day 2: Writing test cases
- Format: Step 1 → Step 2 → Expected result
- Example: "Open login page → enter wrong password → see error message"

**Do:** Write 5 test cases for a login page (correct login, wrong password, empty fields, etc.)

### Day 3: Bug reports
- Title: short description
- Steps: how to reproduce
- Expected vs actual result
- Screenshot/video

**Do:** Find 3 bugs on any website. Write bug reports for each.

### Day 4: Test management
- Tools to organize tests: TestRail, Qase, or even Excel
- Test suites = group of related test cases

**Do:** Put your test cases in a spreadsheet. Tag them (smoke, regression, etc.)

### Day 5: SQL for testers
- `SELECT * FROM users WHERE email = 'test@test.com'`
- Check if data is correct in database

**Do:** Practice SELECT, INSERT, UPDATE queries on a practice DB.

### Day 6-7: Practice
- Test a real website (e.g., a demo e-commerce site)
- Write 10 test cases. Find 5 bugs. File bug reports.

---

## 🗓️ Week 2 — Automation with Playwright

### Day 1: What is automation?
- Instead of clicking manually, you write code that clicks
- Playwright = tool that controls a browser
- You write: "go to this page → click that button → check result"

**Do:** Install Playwright. Open their example. Run it. Watch a browser open and click by itself. Magic.

### Day 2: Your first test
- `page.goto("https://google.com")` — opens Google
- `page.fill("input", "hello")` — types in search box
- `page.click("button")` — clicks search button

**Do:** Write a test that opens Google, searches "cats", and checks results appear.

### Day 3: Assertions (checking things)
- `await expect(page.locator("h1")).toHaveText("Welcome")`
- Test passes if text matches. Fails if not.

**Do:** Write a test that goes to a page and checks the heading text.

### Day 4: Page Object Model
- Instead of writing same code everywhere, put it in reusable files
- `class LoginPage { async login(user, pass) { ... } }`

**Do:** Create a LoginPage class. Use it in 2 different tests.

### Day 5: Testing forms
- Fill input → click submit → check success message

**Do:** Write a test that fills a signup form and verifies success.

### Day 6-7: Build test suite
- 10 tests for a demo site (login, search, add to cart, checkout)
- Run all. See green checkmarks. You're an automation engineer.

---

## 🗓️ Week 3 — API Testing + CI

### Day 1: API testing with Playwright
- `page.request.get("https://api.example.com/users")`
- Check status code, response body

**Do:** Write a test that calls a public API and checks the response.

### Day 2: Postman for API testing
- Postman = tool for testing APIs without code
- Create collections, run tests, see results

**Do:** Create a Postman collection with 5 API tests.

### Day 3: CI/CD (automatic test running)
- Every time you push code, tests run automatically
- GitHub Actions = free CI

**Do:** Set up a GitHub repo. Add a workflow that runs your tests on push.

### Day 4: CI pipeline
- Push code → tests run → green/red status
- Add test reports (Allure or HTML)

**Do:** See your tests run automatically on GitHub. Get a green checkmark.

### Day 5-6: Resume + Portfolio
- GitHub with your test suite (README explaining what it does)
- LinkedIn: "QA Automation Engineer" — add projects

### Day 7: Apply
- Roles: QA Engineer, Test Automation Engineer, SDET
- 10 apps/day

---

## 🗓️ Week 4-5 — Job Hunt

### Day 1-3: Interview prep
- Common questions:
  - "What's the difference between smoke and regression testing?"
  - "How do you report a bug?"
  - "Walk me through your test framework"
- Practice answering out loud

### Day 4-7: Apply + network
- 10-15 apps/day
- LinkedIn: message recruiters at QA roles
- r/softwaretesting, Ministry of Testing community

---

> ✅ **QA is the easiest door into tech.** After 1-2 years, switch to developer if you want. Many devs started in QA.

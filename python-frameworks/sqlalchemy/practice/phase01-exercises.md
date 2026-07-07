# 📝 Phase 01 Practice — SQLAlchemy Core & ORM Foundations

## Exercise 1: Core CRUD

Create a `students` table (id, name, grade, email) using SQLAlchemy Core. Insert 5 students, query those with grade > 80, update one email, delete a student.

**Check:** Run a SELECT after each operation to verify.

## Exercise 2: ORM Models

Define `Author` (id, name, birth_year) and `Book` (id, title, year, author_id FK) using `Mapped`/`mapped_column`. Insert 2 authors and 3 books, then list books by the first author.

**Check:** Verify `book.author.name` works.

## Exercise 3: Query Practice

Using your `Author`/`Book` models, write queries that:
1. Find authors who published after 2000
2. Count books per author
3. Get the author with the most books
4. Order authors by birth_year desc

## Exercise 4: Join Challenge

Create `Customer` (id, name), `Order` (id, customer_id FK, total, date). Write a query that shows each customer's total spending, then another that finds customers who haven't ordered anything.

**Hint:** Use `.outerjoin()` for the second query.

## Exercise 5: Library Integration

Extend the library code (lesson 10) with a `Category` model and link books to categories (many-to-many). Add a query to show all books in a given category.

**Stretch:** Add a `due_date` field to `Loan` and query overdue loans.

# 🏁 Integration: Library Manager
<!-- ⏱️ 25 min | 🔴 Advanced -->

**What You'll Learn:** Combine Core SQL, ORM, relationships, and query patterns into a real library management system.

## Features

- Member management (name, email, join date)
- Book catalog (title, author, ISBN, copies tracking)
- Loan system (borrow, return, availability)
- Statistics (total books, checked out, members)

## Models

```python
class Member(Base):
    loans: Mapped[list["Loan"]] = relationship(back_populates="member")

class Book(Base):
    copies: Mapped[int] = mapped_column(Integer, default=1)
    available: Mapped[int] = mapped_column(Integer, default=1)
    loans: Mapped[list["Loan"]] = relationship(back_populates="book")

class Loan(Base):
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    loan_date: Mapped[date] = mapped_column(default=date.today)
    return_date: Mapped[Optional[date]] = mapped_column(default=None)
```

## Operations

```python
def borrow_book(member_id, book_id):
    book = session.get(Book, book_id)
    if book.available < 1:
        return "Not available"
    book.available -= 1
    session.add(Loan(book_id=book_id, member_id=member_id))
    session.commit()

def return_book(loan_id):
    loan = session.get(Loan, loan_id)
    loan.return_date = date.today()
    loan.book.available += 1
    session.commit()
```

## Key Patterns

- **Availability tracking** — decrement on borrow, increment on return
- **Active loans query** — `filter(Loan.return_date.is_(None))`
- **Stats with aggregates** — `func.sum()`, `func.count()` with group by

## Running the Demo

```bash
python code/10-integration-library.py
```

"""Integration: Library Manager — full CRUD with all core patterns."""
from sqlalchemy import create_engine, String, Integer, Float, Boolean, ForeignKey, Text, DateTime, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship
from datetime import datetime, date
from typing import Optional

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    joined: Mapped[date] = mapped_column(default=date.today)
    loans: Mapped[list["Loan"]] = relationship(back_populates="member")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(100))
    isbn: Mapped[str] = mapped_column(String(20), unique=True)
    copies: Mapped[int] = mapped_column(Integer, default=1)
    available: Mapped[int] = mapped_column(Integer, default=1)
    loans: Mapped[list["Loan"]] = relationship(back_populates="book")

class Loan(Base):
    __tablename__ = "loans"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    loan_date: Mapped[date] = mapped_column(default=date.today)
    return_date: Mapped[Optional[date]] = mapped_column(default=None)
    book: Mapped["Book"] = relationship(back_populates="loans")
    member: Mapped["Member"] = relationship(back_populates="loans")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Seed
session.add_all([
    Member(name="Alice", email="alice@lib.com"),
    Member(name="Bob", email="bob@lib.com"),
])
session.add_all([
    Book(title="Python 101", author="Guide", isbn="001", copies=3, available=3),
    Book(title="SQL Mastery", author="Chen", isbn="002", copies=2, available=2),
    Book(title="Flask Web", author="Jones", isbn="003", copies=1, available=1),
])
session.commit()

print("=" * 50)
print("  LIBRARY MANAGER")
print("=" * 50)

def borrow_book(member_id, book_id):
    book = session.get(Book, book_id)
    member = session.get(Member, member_id)
    if not book or not member:
        return "Member or book not found"
    if book.available < 1:
        return f"'{book.title}' not available"
    loan = Loan(book_id=book_id, member_id=member_id)
    book.available -= 1
    session.add(loan)
    session.commit()
    return f"{member.name} borrowed '{book.title}'"

def return_book(loan_id):
    loan = session.get(Loan, loan_id)
    if not loan or loan.return_date:
        return "Loan not found or already returned"
    loan.return_date = date.today()
    loan.book.available += 1
    session.commit()
    return f"'{loan.book.title}' returned by {loan.member.name}"

def list_loans():
    loans = session.query(Loan).filter(Loan.return_date.is_(None)).all()
    if not loans:
        return "No active loans"
    return [f"{l.member.name} has '{l.book.title}' (since {l.loan_date})" for l in loans]

def list_books():
    books = session.query(Book).all()
    return [f"[{b.id}] {b.title:25s} by {b.author:15s} ({b.available}/{b.copies} avail)" for b in books]

print("\n1. Library catalog:")
for l in list_books():
    print(f"   {l}")

print("\n2. Borrowing:")
print(f"   {borrow_book(1, 1)}")
print(f"   {borrow_book(1, 2)}")
print(f"   {borrow_book(2, 1)}")

print("\n3. Active loans:")
for l in list_loans():
    print(f"   {l}")

print(f"\n4. Return book 1:")
loan = session.query(Loan).filter(Loan.book_id == 1, Loan.return_date.is_(None)).first()
print(f"   {return_book(loan.id)}")

print(f"\n5. Catalog after return:")
for l in list_books():
    print(f"   {l}")

print(f"\n6. Stats:")
stats = session.query(
    func.count(Member.id).label("members"),
    func.sum(Book.copies).label("total_books"),
    func.sum(Book.copies - Book.available).label("checked_out"),
).first()
print(f"   Members: {stats.members}, Books: {stats.total_books}, Checked out: {stats.checked_out}")
session.close()
print("\n✅ Library Manager complete")

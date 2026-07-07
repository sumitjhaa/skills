# 📘 Django Phase 02 — Lesson 08: Model Inheritance

> 🎯 **Goal**: Understand Django's three inheritance styles: abstract, multi-table, and proxy models.

## 📖 Concepts

### 1. Abstract Base Classes
No separate DB table. Fields are **copied into child tables**.

```python
class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        abstract = True  # ← no Person table

class Student(Person):
    student_id = models.CharField(max_length=20)
    grade = models.IntegerField()

class Teacher(Person):
    employee_id = models.CharField(max_length=20)
    subject = models.CharField(max_length=50)
```

**DB tables**: `student` (name, email, student_id, grade), `teacher` (name, email, employee_id, subject)

**Use when**: You want shared fields but no polymorphism or shared queries.

### 2. Multi-Table Inheritance
Each model gets its own table with an implicit `OneToOneField` to the parent.

```python
class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=True)
    serves_pizza = models.BooleanField(default=False)
```

**DB tables**: `place` (id, name, address), `restaurant` (place_ptr_id, serves_hot_dogs, serves_pizza)

**Use when**: You need polymorphism (query base or child, `isinstance()` checks).

**Caution**: JOIN overhead on every child query.

### 3. Proxy Models
Same table, different Python behavior. No new table.

```python
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    is_public = models.BooleanField(default=True)

class PublicEvent(Event):
    class Meta:
        proxy = True  # ← no new table

    def __str__(self):
        return f"[Public] {self.name}"
```

**Use when**: Different Python interface to the same data (custom managers, methods, default ordering).

### Comparison

| Style | New Table | Parent Fields | Polymorphism | Use Case |
|-------|-----------|---------------|--------------|----------|
| Abstract | No (per child) | Copied | No | Share fields |
| Multi-Table | Yes (each) | FK via OneToOne | Yes | Different behavior + shared queries |
| Proxy | No | Same table | No | Different Python interface |

### ADHD-Friendly Summary
```
Abstract   → no parent table, fields copied to children
Multi-table → parent table + child table, linked by OneToOne
Proxy      → same table, different class behavior
```

## 🛠️ Code

```python
# Abstract
class Person(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        abstract = True

class Student(Person):
    grade = models.IntegerField()
# Table: student (id, name, grade)

# Multi-table
class Place(models.Model):
    name = models.CharField(max_length=100)

class Restaurant(Place):
    pizza = models.BooleanField()
# Tables: place (id, name), restaurant (place_ptr_id, pizza)

# Proxy
class Event(models.Model):
    name = models.CharField(max_length=100)

class PublicEvent(Event):
    class Meta:
        proxy = True
# Table: event (id, name) — both classes use the same table
```

## 🧪 Practice

1. Create abstract `Content` base with `title`, `created_at`
2. Create `Article(Content)` and `Video(Content)` with their own fields
3. Create multi-table `User` and `Admin(User)` where Admin has extra permissions
4. Create a proxy `PublishedPost` that only shows published posts by default

## 🧠 Key Takeaways

- Abstract is for **DRY fields** — no polymorphism
- Multi-table is for **polymorphism** — at the cost of JOINs
- Proxy is for **different Python behaviors** on the same table
- Proxy models can have different `ordering`, `managers`, or custom methods
- Multi-table inheritance has implicit OneToOne — `restaurant.place` works both ways

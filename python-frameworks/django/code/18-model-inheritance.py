"""Model inheritance: abstract base, multi-table, proxy models."""


# ======================== 1. Abstract Base Class ========================

class PersonBase:
    _abstract = True
    _fields = []

    def __init__(self, **kwargs):
        for fname in self._fields:
            setattr(self, f'_{fname}', kwargs.get(fname))


class Student(PersonBase):
    _fields = ["name", "email", "student_id", "grade"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self): return self._name
    @property
    def email(self): return self._email
    @property
    def student_id(self): return self._student_id
    @property
    def grade(self): return self._grade


class Teacher(PersonBase):
    _fields = ["name", "email", "employee_id", "subject"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self): return self._name
    @property
    def email(self): return self._email
    @property
    def employee_id(self): return self._employee_id
    @property
    def subject(self): return self._subject


# ======================== 2. Multi-Table Inheritance ========================

class Place:
    def __init__(self, name="", address=""):
        self.name = name
        self.address = address


class Restaurant(Place):
    def __init__(self, name="", address="", serves_hot_dogs=True, serves_pizza=False):
        super().__init__(name, address)
        self.serves_hot_dogs = serves_hot_dogs
        self.serves_pizza = serves_pizza


# ======================== 3. Proxy Model ========================

class Event:
    def __init__(self, name="", date="", is_public=True):
        self.name = name
        self.date = date
        self.is_public = is_public

    def __repr__(self):
        return f"Event: {self.name}"


class PublicEvent(Event):
    """Proxy — same table, different behavior."""
    def __repr__(self):
        return f"PublicEvent: {self.name} (public)"


# ======================== Usage ========================

print("=== 1. Abstract Base Inheritance ===")
alice = Student(name="Alice", email="alice@uni.edu", student_id="S001", grade=90)
bob = Teacher(name="Bob", email="bob@school.edu", employee_id="T001", subject="Math")

print(f"  Student: {alice.name}, grade={alice.grade}")
print(f"  Teacher: {bob.name}, subject={bob.subject}")

# Fields live on each child table (no shared Person table)
print(f"  Student fields: {Student._fields}")
print(f"  Teacher fields: {Teacher._fields}")

print("\n=== 2. Multi-Table Inheritance ===")
p = Place("Central Park", "NYC")
r = Restaurant("Pizza Place", "Main St", serves_pizza=True)
print(f"  Place: {p.name} @ {p.address}")
print(f"  Restaurant: {r.name}, pizza={r.serves_pizza}, hot_dogs={r.serves_hot_dogs}")
# Restaurant has its own table + Place's fields
print(f"  isinstance(r, Place): {isinstance(r, Place)}")
print(f"  isinstance(r, Restaurant): {isinstance(r, Restaurant)}")

print("\n=== 3. Proxy Model ===")
e1 = Event("Conference", "2024-07-01")
e2 = PublicEvent("Workshop", "2024-09-01")
print(f"  {e1}")
print(f"  Proxy: {e2}")
# Same DB table, different Python behavior
print(f"  isinstance(e2, Event): {isinstance(e2, Event)}")
print(f"  type(e2).__name__: {type(e2).__name__}")

"""Phase 07 — Practice Solutions"""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from enum import Enum, auto, unique


# ─── Exercise 1: Bank Account ────────────────────────────────────────────────

class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = initial_balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount


acc = BankAccount("Alice", 1000)
acc.deposit(500)
acc.withdraw(200)
assert acc.balance == 1300.0
print("1. BankAccount OK")

# ─── Exercise 2: Library System ──────────────────────────────────────────────

@dataclass(frozen=True)
class Book:
    title: str
    author: str
    isbn: str
    year: int


class Library:
    def __init__(self):
        self._books: dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            raise ValueError(f"ISBN {book.isbn} exists")
        self._books[book.isbn] = book

    def remove_book(self, isbn: str) -> None:
        if isbn not in self._books:
            raise ValueError(f"No book with ISBN {isbn}")
        del self._books[isbn]

    def search_by_author(self, author: str) -> list[Book]:
        return [b for b in self._books.values() if b.author == author]

    def total_books(self) -> int:
        return len(self._books)


lib = Library()
lib.add_book(Book("1984", "Orwell", "1", 1949))
lib.add_book(Book("Animal Farm", "Orwell", "2", 1945))
assert lib.total_books() == 2
assert len(lib.search_by_author("Orwell")) == 2
print("2. Library OK")

# ─── Exercise 3: Vehicle Hierarchy ───────────────────────────────────────────

class Vehicle(ABC):
    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year

    @abstractmethod
    def fuel_efficiency(self) -> float:
        pass


class Car(Vehicle):
    def __init__(self, make: str, model: str, year: int, mpg: float):
        super().__init__(make, model, year)
        self.mpg = mpg

    def fuel_efficiency(self) -> float:
        return self.mpg


class ElectricCar(Vehicle):
    def __init__(self, make: str, model: str, year: int, mpkwh: float):
        super().__init__(make, model, year)
        self.mpkwh = mpkwh

    def fuel_efficiency(self) -> float:
        return self.mpkwh


class Motorcycle(Vehicle):
    def __init__(self, make: str, model: str, year: int, mpg: float):
        super().__init__(make, model, year)
        self.mpg = mpg

    def fuel_efficiency(self) -> float:
        return self.mpg * 1.2


v: list[Vehicle] = [Car("Toyota", "Camry", 2020, 32), ElectricCar("Tesla", "3", 2023, 4.5)]
assert len(v) == 2
print("3. Vehicle OK")

# ─── Exercise 4: Shape Area ──────────────────────────────────────────────────

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h

    def area(self) -> float:
        return self.w * self.h

    def perimeter(self) -> float:
        return 2 * (self.w + self.h)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


def total_area(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)


shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
assert round(total_area(shapes), 1) == 108.5
print("4. Shape OK")

# ─── Exercise 5: E-commerce Cart ─────────────────────────────────────────────

class ECommerceCart:
    tax_rate = 0.08

    def __init__(self):
        self._items: dict[str, dict] = {}

    def add_item(self, name: str, price: float, qty: int = 1) -> None:
        if name in self._items:
            self._items[name]["qty"] += qty
        else:
            self._items[name] = {"price": price, "qty": qty}

    def remove_item(self, name: str) -> None:
        self._items.pop(name, None)

    @property
    def total(self) -> float:
        subtotal = sum(i["price"] * i["qty"] for i in self._items.values())
        return subtotal * (1 + self.tax_rate)

    def __len__(self) -> int:
        return sum(i["qty"] for i in self._items.values())

    def __str__(self) -> str:
        lines = [f"{n}: ${i['price']:.2f} × {i['qty']}" for n, i in self._items.items()]
        return "\n".join(lines) + f"\nTotal (with tax): ${self.total:.2f}"

    @classmethod
    def from_promo_code(cls, code: str, items: list[tuple[str, float, int]]):
        cart = cls()
        for name, price, qty in items:
            cart.add_item(name, price, qty)
        return cart


cart = ECommerceCart()
cart.add_item("Laptop", 1200, 1)
cart.add_item("Mouse", 25, 2)
assert abs(cart.total - 1350.0) < 0.01
print("5. Cart OK")

# ─── Exercise 6: Game Character ──────────────────────────────────────────────

class Weapon:
    def __init__(self, name: str, damage: int, element: str = "none"):
        self.name = name
        self.damage = damage
        self.element = element

    def bonus_vs(self, target_element: str) -> int:
        return self.damage if self.element == target_element else 0


class Character:
    __slots__ = ("name", "health", "level", "xp", "weapon", "_inventory")

    def __init__(self, name: str, health: int, level: int = 1):
        self.name = name
        self.health = health
        self.level = level
        self.xp = 0
        self.weapon = Weapon("Fists", 5)
        self._inventory: list[str] = []

    def attack(self, target_element: str = "none") -> int:
        return self.weapon.damage + self.weapon.bonus_vs(target_element)


hero = Character("Lyra", 100)
hero.weapon = Weapon("Flame Sword", 25, "fire")
frost_enemy = hero.attack("fire")  # bonus vs fire! ... wait, bonus vs target element
assert hero.attack("water") == 25  # no bonus
print("6. Character OK")

# ─── Exercise 7: Social Media Feed ───────────────────────────────────────────

class Post:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author
        self.likes = 0
        self.comments: list[str] = []

    def __add__(self, comment: str) -> "Post":
        self.comments.append(comment)
        return self

    def __gt__(self, other: "Post") -> bool:
        return self.likes > other.likes

    def __contains__(self, word: str) -> bool:
        return word.lower() in self.content.lower()

    def add_like(self) -> None:
        self.likes += 1

    @property
    def popularity(self) -> int:
        return self.likes + len(self.comments) * 2


p1 = Post("Python is awesome!", "Alice")
p2 = Post("Learning OOP", "Bob")
p1.add_like()
p1.add_like()
p2.add_like()
p1 + "Great post!" + "Totally agree!"
assert "Python" in p1
assert p1.popularity == 6
print("7. Social OK")

# ─── Exercise 8: SOLID Refactor ──────────────────────────────────────────────

@dataclass
class Invoice:
    items: list[float]
    tax_rate: float

    def total(self) -> float:
        return sum(self.items) * (1 + self.tax_rate)


class InvoicePrinter:
    @staticmethod
    def print_pdf(inv: Invoice) -> str:
        return f"PDF: ${inv.total():.2f}"

    @staticmethod
    def print_html(inv: Invoice) -> str:
        return f"<p>${inv.total():.2f}</p>"


class InvoiceRepository:
    @staticmethod
    def save(inv: Invoice) -> str:
        return f"Saving invoice ${inv.total():.2f} to DB"


class InvoiceMailer:
    @staticmethod
    def send(inv: Invoice) -> str:
        return f"Emailing invoice ${inv.total():.2f}"


inv = Invoice([100, 200, 50], 0.08)
assert InvoicePrinter.print_pdf(inv).startswith("PDF:")
print("8. SOLID OK")

# ─── Exercise 9: Plugin Registry ─────────────────────────────────────────────

class FileParser:
    registry: dict[str, type["FileParser"]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ext = getattr(cls, "extension", cls.__name__.lower().replace("parser", ""))
        cls.extension = ext
        FileParser.registry[ext] = cls

    def parse(self, content: str) -> dict:
        raise NotImplementedError


class CsvParser(FileParser):
    extension = "csv"
    def parse(self, content: str) -> dict:
        return {"format": "csv", "rows": content.strip().split("\n")}


class JsonParser(FileParser):
    extension = "json"
    def parse(self, content: str) -> dict:
        return {"format": "json", "content": content}


class YamlParser(FileParser):
    extension = "yaml"
    def parse(self, content: str) -> dict:
        return {"format": "yaml", "content": content}


def parse_file(filename: str, content: str) -> dict:
    ext = filename.rsplit(".", 1)[-1]
    parser_cls = FileParser.registry.get(ext)
    if not parser_cls:
        raise ValueError(f"No parser for .{ext}")
    return parser_cls().parse(content)


result = parse_file("data.csv", "a,b,c\n1,2,3")
assert result["format"] == "csv"
print("9. Plugin OK")

# ─── Exercise 10: Enum State Machine ─────────────────────────────────────────

@unique
class TrafficLight(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()

    def next_light(self) -> "TrafficLight":
        order = [TrafficLight.RED, TrafficLight.GREEN, TrafficLight.YELLOW]
        idx = order.index(self)
        return order[(idx + 1) % len(order)]

    def can_cross(self) -> bool:
        return self == TrafficLight.GREEN


light = TrafficLight.RED
assert not light.can_cross()
assert light.next_light() == TrafficLight.GREEN
green = TrafficLight.GREEN
assert green.can_cross()
assert green.next_light() == TrafficLight.YELLOW
print("10. Enum OK")

# ─── Exercise 11: Custom Range ────────────────────────────────────────────────

class Range:
    def __init__(self, start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        self._start = start
        self._stop = stop
        self._step = step
        self._data = list(range(start, stop, step))

    def __contains__(self, n):
        return n in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, i):
        return self._data[i]

    def __reversed__(self):
        return Range(self._data[-1], self._start - self._step, -self._step)


r = Range(0, 10, 2)
assert 4 in r
assert 5 not in r
assert len(r) == 5
assert r[0] == 0
assert r[-1] == 8
assert list(reversed(r)) == [8, 6, 4, 2, 0]
print("11. Range OK")

# ─── Exercise 12: Money with Full Operators ───────────────────────────────────

class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount:.2f} {self.currency})"

    def __eq__(self, other):
        if isinstance(other, Money):
            return self.amount == other.amount and self.currency == other.currency
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount < other.amount
        return NotImplemented

    def __neg__(self):
        return Money(-self.amount, self.currency)

    def __abs__(self):
        return Money(abs(self.amount), self.currency)

    def __add__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(self.amount + other.amount, self.currency)
        raise ValueError(f"Currency mismatch: {self.currency} vs {other.currency}")

    def __sub__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(self.amount - other.amount, self.currency)
        raise ValueError(f"Currency mismatch: {self.currency} vs {other.currency}")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Money(self.amount * scalar, self.currency)
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Money(self.amount / scalar, self.currency)
        return NotImplemented


m1 = Money(100, "USD")
m2 = Money(50, "USD")
assert m1 + m2 == Money(150, "USD")
assert m1 - m2 == Money(50, "USD")
assert m1 * 2 == Money(200, "USD")
assert 3 * m1 == Money(300, "USD")
assert m1 / 2 == Money(50, "USD")
assert -m1 == Money(-100, "USD")
assert abs(Money(-50)) == Money(50)
assert m2 < m1
print("12. Money OK")

# ─── Exercise 13: PlayingCard with match/case ─────────────────────────────────

class PlayingCard:
    __match_args__ = ("rank", "suit")

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def describe(self):
        return f"{self.rank} of {self.suit}"


card = PlayingCard("Ace", "Spades")
assert card.describe() == "Ace of Spades"

matched = False
match card:
    case PlayingCard("Ace", "Spades"):
        matched = True
    case PlayingCard(rank, suit):
        pass

assert matched

match card:
    case PlayingCard(rank, "Hearts"):
        result = "hearts"
    case PlayingCard("King", suit):
        result = "king"
    case PlayingCard(rank, suit):
        result = f"{rank} of {suit}"

assert result == "Ace of Spades"
print("13. PlayingCard OK")

# ─── Exercise 14: CustomPath with fspath ──────────────────────────────────────

import os

class CustomPath:
    def __init__(self, path):
        self._path = path

    def __fspath__(self):
        return self._path

    def __format__(self, fmt):
        if fmt == "abs":
            return os.path.abspath(self._path)
        return self._path

    def __str__(self):
        return self._path

    def __repr__(self):
        return f"CustomPath({self._path!r})"


p = CustomPath("/tmp")
assert os.path.exists(p)
assert isinstance(os.fspath(p), str)
assert f"{p:abs}" == "/tmp"
print("14. CustomPath OK")

# ─── Exercise 15: Logger with Destructor ─────────────────────────────────────

import tempfile
from datetime import datetime

class Logger:
    def __init__(self, filename):
        self._file = open(filename, "w")

    def log(self, message):
        ts = datetime.now().isoformat()
        self._file.write(f"[{ts}] {message}\n")
        self._file.flush()

    def __del__(self):
        if hasattr(self, "_file") and not self._file.closed:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.__del__()
        return False


with Logger("/tmp/test_log.txt") as log:
    log.log("Test message")

import os
assert os.path.exists("/tmp/test_log.txt")
with open("/tmp/test_log.txt") as f:
    content = f.read()
assert "Test message" in content
os.remove("/tmp/test_log.txt")
print("15. Logger OK")

# ─── Exercise 16: Subscription Pricing with @property ─────────────────────────

import functools
from dataclasses import field

class Subscription:
    VALID_PLANS = ("basic", "premium", "enterprise")

    def __init__(self, plan: str, monthly_fee: float, discount_pct: float = 0):
        self._plan = plan
        self._monthly_fee = monthly_fee
        self._discount_pct = discount_pct

    @property
    def plan(self) -> str:
        return self._plan

    @plan.setter
    def plan(self, value: str) -> None:
        if value not in self.VALID_PLANS:
            raise ValueError(f"Invalid plan {value!r}, choose from {self.VALID_PLANS}")
        self._plan = value

    @property
    def monthly_fee(self) -> float:
        return self._monthly_fee

    @monthly_fee.setter
    def monthly_fee(self, value: float) -> None:
        if value < 0:
            raise ValueError(f"Fee must be non-negative, got {value}")
        self._monthly_fee = value
        self.__dict__.pop("tax_rate", None)

    @property
    def discount(self) -> float:
        return self._discount_pct

    @discount.setter
    def discount(self, value: float) -> None:
        if not 0 <= value <= 100:
            raise ValueError(f"Discount must be 0-100%, got {value}")
        self._discount_pct = value
        self.__dict__.pop("tax_rate", None)

    @property
    def annual_cost(self) -> float:
        return round(12 * self._monthly_fee * (1 - self._discount_pct / 100), 2)

    @functools.cached_property
    def tax_rate(self) -> float:
        return 0.08


sub = Subscription("premium", 29.99, 10)
assert sub.annual_cost == 323.89
assert sub.tax_rate == 0.08
sub.discount = 20
assert sub.annual_cost == 287.90
try:
    sub.monthly_fee = -5
except ValueError:
    pass
print("16. Subscription OK")

# ─── Exercise 17: Employee Directory with @dataclass ──────────────────────────

@dataclass(order=True)
class Employee:
    emp_id: str
    name: str
    department: str
    salary: float = field(metadata={"currency": "USD"})
    skills: list[str] = field(default_factory=list, compare=False)
    _notes: str = field(default="", repr=False)

    def __post_init__(self):
        if self.salary < 0:
            raise ValueError(f"Salary must be non-negative, got {self.salary}")
        if not self.department:
            raise ValueError("Department cannot be empty")


emps = [
    Employee("E1", "Alice", "Engineering", 120000, ["Python", "K8s"]),
    Employee("E2", "Bob", "Marketing", 90000, ["SEO"]),
    Employee("E3", "Charlie", "Engineering", 110000, ["Go", "Docker"]),
]
sorted_emps = sorted(emps)
assert sorted_emps[0].name == "Alice"  # Sorted by emp_id: E1 < E2 < E3
alice_new = replace(emps[0], salary=130000)
assert alice_new.salary == 130000
assert alice_new.skills == emps[0].skills
print("17. Employee OK")

# ─── Exercise 18: Order Status Machine with Enum ──────────────────────────────

class OrderStatus(Enum):
    PENDING = (auto(), ["CONFIRMED", "CANCELLED"])
    CONFIRMED = (auto(), ["SHIPPED", "CANCELLED"])
    SHIPPED = (auto(), ["DELIVERED"])
    DELIVERED = (auto(), [])
    CANCELLED = (auto(), [])

    def __new__(cls, _, transitions):
        obj = object.__new__(cls)
        obj._value_ = _
        obj.transitions = transitions
        return obj

    def transition(self, next_status: "OrderStatus") -> "OrderStatus":
        if next_status.name not in self.transitions:
            raise ValueError(f"Cannot transition from {self.name} to {next_status.name}")
        return next_status

    @property
    def is_terminal(self) -> bool:
        return self in (OrderStatus.DELIVERED, OrderStatus.CANCELLED)


status = OrderStatus.PENDING
status = status.transition(OrderStatus.CONFIRMED)
assert status == OrderStatus.CONFIRMED
status = status.transition(OrderStatus.SHIPPED)
assert status == OrderStatus.SHIPPED
status = status.transition(OrderStatus.DELIVERED)
assert status.is_terminal
try:
    OrderStatus.DELIVERED.transition(OrderStatus.PENDING)
except ValueError:
    pass
print("18. OrderStatus OK")

# ─── Exercise 19: Temperature Sensor with Descriptors ─────────────────────────

class Celsius:
    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._name, 0.0) - 273.15

    def __set__(self, obj, value):
        kelvin = value + 273.15
        if kelvin < 0:
            raise ValueError(f"Temperature {value}°C is below absolute zero")
        setattr(obj, self._name, kelvin)


class Fahrenheit:
    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        celsius = getattr(obj, self._name, 273.15) - 273.15
        return celsius * 9 / 5 + 32

    def __set__(self, obj, value):
        celsius = (value - 32) * 5 / 9
        kelvin = celsius + 273.15
        if kelvin < 0:
            raise ValueError(f"Temperature {value}°F is below absolute zero")
        setattr(obj, self._name, kelvin)


class TemperatureSensor:
    celsius = Celsius()
    fahrenheit = Fahrenheit()

    def __init__(self, location: str, celsius: float, fahrenheit: float):
        self.location = location
        self.celsius = celsius
        self.fahrenheit = fahrenheit


sensor = TemperatureSensor("Lab-1", 25.0, 77.0)
assert abs(sensor.celsius - 25.0) < 0.1
assert abs(sensor.fahrenheit - 77.0) < 0.1
try:
    sensor.celsius = -300
except ValueError:
    pass
try:
    sensor.fahrenheit = -500
except ValueError:
    pass
print("19. Temperature OK")

print("\n=== All solutions passed! ===")

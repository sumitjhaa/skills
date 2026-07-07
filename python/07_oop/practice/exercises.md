# 🏋️ Practice Exercises — Phase 07: OOP

Mixed difficulty. Use real-world domains.

## Exercise 1: Bank Account (🟢)
Create a `BankAccount` class with `owner`, `balance` (private), and methods `deposit(amount)`, `withdraw(amount)`. Add a `@property` for `balance` (read-only). Validate deposits/withdrawals are positive and withdrawals don't exceed balance.

## Exercise 2: Library System (🟢)
Create a `Book` dataclass with `title`, `author`, `isbn`, `year`. Create a `Library` class that composes `Book` objects. Implement `add_book`, `remove_book(isbn)`, `search_by_author(author)`, and `total_books()`. Ensure no duplicate ISBNs.

## Exercise 3: Vehicle Hierarchy (🟡)
Create `Vehicle` base class with `make`, `model`, `year`, and `fuel_efficiency()` (abstract). Implement `Car` (miles per gallon), `ElectricCar` (miles per kWh), and `Motorcycle`. Use `super()` in constructors. Each subclass implements `fuel_efficiency()` differently.

## Exercise 4: Shape Area Calculator (🟡)
Create a `Shape` ABC with `@abstractmethod area()` and `perimeter()`. Implement `Circle`, `Rectangle`, `Triangle`. Write a function `total_area(shapes: list[Shape])` that uses polymorphism. Test with a mix of shapes.

## Exercise 5: E-commerce Cart (🟡)
Build an `ECommerceCart` class with:
- `add_item(name, price, qty)` — adds/replaces items
- `remove_item(name)` — removes item
- `total` property — computes total with 8% tax
- `__len__` — returns item count
- `__str__` — pretty-prints the cart
- `@classmethod from_promo_code(cls, code, items)` — applies a discount

## Exercise 6: Game Character Builder (🟡)
Create a `GameCharacter` class with slots (`name`, `health`, `level`, `xp`). Add a `Mage(Character)` subclass with `mana` attribute. Use composition: each character has a `Weapon` (name, damage, element) and `Inventory` (list of potions). Implement `attack()` to use weapon damage + element bonus.

## Exercise 7: Social Media Feed (🟡)
Create `Post` and `Comment` classes. `Post` has: `content`, `author`, `likes`, `comments` list. Implement:
- `__add__(comment)` — adds a comment
- `__gt__(other)` — compares by likes
- `__contains__(word)` — checks if word is in content
- `add_like()` method
- `@property popularity` — likes + comments_count * 2

## Exercise 8: SOLID Refactor (🔴)
Refactor this code to follow SRP and OCP:

```python
class Invoice:
    def __init__(self, items, tax_rate):
        self.items = items
        self.tax_rate = tax_rate

    def total(self):
        return sum(self.items) * (1 + self.tax_rate)

    def print_pdf(self):
        print(f"PDF: ${self.total():.2f}")

    def print_html(self):
        print(f"<p>${self.total():.2f}</p>")

    def save_to_db(self):
        print("Saving to database...")

    def send_email(self):
        print("Emailing invoice...")
```

Split into `Invoice` (data), `InvoicePrinter` (PDF/HTML), `InvoiceRepository` (DB), `InvoiceMailer` (email).

## Exercise 9: Plugin Registry with \_\_init\_subclass\_\_ (🔴)
Create a `FileParser` base class with `__init_subclass__` that auto-registers parsers by file extension. Implement `CsvParser` (`.csv`), `JsonParser` (`.json`), `YamlParser` (`.yaml`). Include a `parse(filename)` factory function that selects the right parser.

## Exercise 10: Enum State Machine (🔴)
Create a `TrafficLight` enum with `RED`, `YELLOW`, `GREEN`. Add a `next_light()` method (as either an enum method or a standalone function) that returns the next state. Implement `can_cross()` that returns `True` only for `GREEN`. Use `@unique` to prevent duplicates.

---

## Advanced Nitigrities

## Exercise 16: Subscription Pricing with @property (🟡)
Create a `Subscription` class with `_plan` (str), `_monthly_fee` (float), and `_discount_pct` (float). Implement:
- `@property plan` with setter that validates plan is one of: `"basic"`, `"premium"`, `"enterprise"`
- `@property monthly_fee` with setter that rejects negative values
- `@property discount` with setter that validates 0–100%
- `@property annual_cost` — computed: 12 × monthly_fee × (1 − discount/100)
- `@functools.cached_property tax_rate` — returns fixed 0.08 (simulating a config lookup)
- Clear cache when any price-affecting property changes (use `__dict__.pop("tax_rate", None)`)

## Exercise 17: Employee Directory with @dataclass (🟡)
Create a `@dataclass(order=True)` `Employee` with: `emp_id: str`, `name: str`, `department: str`, `salary: float`, `skills: list[str] = field(default_factory=list, compare=False)`, `_notes: str = field(default="", repr=False)`. Use `metadata={"currency": "USD"}` on salary. In `__post_init__`, validate salary ≥ 0 and department is non-empty. Demonstrate `sorted()` and `replace()`.

## Exercise 18: Order Status Machine with Enum (🔴)
Create an `OrderStatus(Enum)` with `PENDING`, `CONFIRMED`, `SHIPPED`, `DELIVERED`, `CANCELLED`. Use `auto()`. Each member stores a list of valid transitions (e.g., `PENDING → ["CONFIRMED", "CANCELLED"]`). Implement `transition(self, next_status)` that raises `ValueError` on invalid transitions. Add `@property is_terminal` that returns `True` for `DELIVERED` and `CANCELLED`. Demonstrate at least 3 transitions and 1 invalid one.

## Exercise 19: Temperature Sensor with Descriptors (🔴)
Create a `Celsius` descriptor that validates temperature ≥ −273.15 (absolute zero) and stores values as Kelvin internally. Create a `Fahrenheit` descriptor that converts to/from Celsius on the fly (stores Kelvin, returns Fahrenheit). Use in a `TemperatureSensor(location, celsius_reading, fahrenheit_reading)` class. Demonstrate setting/getting both scales, and catching an error when going below absolute zero.

---

# Dunder Methods & Operator Overloading Exercises

# Dunder Methods & Operator Overloading Exercises

## Exercise 11: Custom Range (🟡)
Write a `Range` class that mimics `range()` but supports:
- `__contains__` — check if a number is in the range
- `__reversed__` — return a new Range in reverse
- `__len__` — count of numbers
- `__getitem__` — index into the range (negative indexing too)

## Exercise 12: Money with Full Operators (🟡)
Create a `Money(amount, currency)` class with:
- `__add__` / `__sub__` — same currency only (raise `ValueError` on mismatch)
- `__mul__` / `__rmul__` — multiply by scalar (int/float)
- `__truediv__` — divide by scalar
- `__neg__` / `__abs__`
- `__eq__` / `__lt__` — comparisons, same currency only
- `__repr__` — e.g., `Money(100.00 USD)`

## Exercise 13: PlayingCard with match/case (🟡)
Create a `PlayingCard` class with `__match_args__ = ("rank", "suit")` that supports `match/case` destructuring. Add a `describe()` method that returns the card name. Demonstrate `match card:` with at least two patterns.

## Exercise 14: CustomPath with fspath (🟡)
Create a `CustomPath` class that wraps a string path and implements `__fspath__` so it works with `os.path.exists()`, `os.path.getsize()`, and `open()`. Also implement `__format__` to support `f"{path:abs}"` for absolute path.

## Exercise 15: Logger with Destructor (🔴)
Create a `Logger` class that:
- Opens a file handle on init
- Implements `__del__` to flush and close the file
- Has a `log(message)` method that writes timestamps
- Implements `__enter__` / `__exit__` for context manager use
- Demonstrates both `with` block usage and explicit cleanup

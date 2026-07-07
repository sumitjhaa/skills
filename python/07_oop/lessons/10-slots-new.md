# 🎯 Slots & New
<!-- ⏱️ 14 min read | 🟡 Core | 🧠 Core -->

**What You'll Learn:** Reduce memory with `__slots__`, understand `__new__` vs `__init__`, and implement the singleton pattern.

> 💡 **TL;DR — The whole point:** `__slots__` eliminates the per-instance `__dict__` to save memory. `__new__` creates objects before `__init__` initializes them.

## 🔗 Why This Matters
If you're creating millions of particle effects in a game or sensor readings in a data pipeline, `__slots__` can cut memory usage by 60%+. `__new__` is how you control object creation itself — useful for singletons, caching, and immutable objects.

## The Concept
`__slots__` tells Python to store attributes in a fixed array instead of a dictionary. `__new__` is the static method that allocates memory; `__init__` initializes it. `__new__` runs first.

## Code Example
```python
"""Gaming: Particle system with __slots__ and a singleton GameEngine."""


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "lifetime")

    def __init__(self, x: float, y: float, vx: float, vy: float, lifetime: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime

    def update(self) -> bool:
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime > 0


class GameEngine:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name: str = "Engine"):
        if not self._initialized:
            self.name = name
            self.particles: list[Particle] = []
            GameEngine._initialized = True

    def spawn_particles(self, count: int) -> None:
        for _ in range(count):
            self.particles.append(Particle(0, 0, 1, 1, 100))

    @property
    def particle_count(self) -> int:
        return len(self.particles)


engine1 = GameEngine("Main Engine")
engine2 = GameEngine()

print(f"Same engine? {engine1 is engine2}")
print(f"Engine name: {engine1.name}")

engine1.spawn_particles(1000)
print(f"Particles: {engine1.particle_count}")
print(f"Particle has __dict__? {'__dict__' in dir(Particle)}")

try:
    p = Particle(0, 0, 1, 1, 100)
    p.extra = "not allowed"
except AttributeError as e:
    print(f"Can't add extra attr: {e}")
```

## 🔍 How It Works
- `__slots__ = ("x", "y", ...)` replaces `__dict__` with a tuple of allowed attribute names
- Slots attributes are stored in a compact array — faster access, less memory
- `__new__` creates the object; `__init__` initializes it. `__new__` is called first
- Singleton pattern: `__new__` checks for an existing instance and returns it
- `__slots__` breaks multiple inheritance unless every class in the chain uses them

## ⚠️ Common Pitfall
Slots classes can't have `__dict__`. If you need dynamic attributes, don't use `__slots__`. Also, slots classes can't be used with `@dataclass` (unless `@dataclass(slots=True)` in Python 3.10+).

## 🧠 Memory Aid
"`__slots__` = fixed parking spots (no valet). `__new__` = the factory that makes the car. `__init__` = the detailer that cleans it."

## 🏃 Try It
Create a `Vector3D` class with `__slots__ = ("x", "y", "z")`. Add `__add__` and `__abs__` methods. Create 10,000 instances and see how memory compares to a dict-based version.

## 🔗 Related
- [Classes & Objects](01-classes-objects.md) — object creation lifecycle
- [OOP Design](11-oop-design.md) — patterns & trade-offs

## ➡️ Next
[OOP Design](11-oop-design.md)

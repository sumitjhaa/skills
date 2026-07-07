"""07-10-slots-new.py — Gaming: Particle with __slots__ and singleton GameEngine."""

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

p = Particle(0, 0, 1, 1, 100)
try:
    p.extra = "not allowed"
except AttributeError as e:
    print(f"No dynamic attrs with __slots__: {e}")

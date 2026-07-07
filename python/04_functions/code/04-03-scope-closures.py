"""Game state management with closures — health bars and counters."""


def create_health_bar(max_hp: int):
    current_hp = max_hp

    def take_damage(amount: int) -> int:
        nonlocal current_hp
        current_hp = max(0, current_hp - amount)
        return current_hp

    def heal(amount: int) -> int:
        nonlocal current_hp
        current_hp = min(max_hp, current_hp + amount)
        return current_hp

    def status() -> str:
        bar = "█" * current_hp + "░" * (max_hp - current_hp)
        return f"HP: [{bar}] {current_hp}/{max_hp}"

    return {"damage": take_damage, "heal": heal, "status": status}


def make_counter(start: int = 0):
    count = start

    def increment(step: int = 1) -> int:
        nonlocal count
        count += step
        return count

    return increment


def make_player(name: str):
    score = 0

    def get_name() -> str:
        return name

    def add_score(points: int) -> int:
        nonlocal score
        score += points
        return score

    def get_score() -> int:
        return score

    return {"get_name": get_name, "add_score": add_score, "get_score": get_score}


player = create_health_bar(100)
print(player["status"]())
player["damage"](30)
print(player["status"]())
player["heal"](15)
print(player["status"]())

score = make_counter(0)
print(score())
print(score(5))

alice = make_player("Alice")
print(alice["get_name"]())
alice["add_score"](10)
print(alice["get_score"]())

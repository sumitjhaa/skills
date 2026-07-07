"""Phase 04 Integration: One Piece Bounty System — all function concepts combined."""

from functools import reduce, wraps, lru_cache
import time

CREW = [
    {"name": "Monkey D. Luffy",    "role": "Captain",       "bounty": 3_000_000_000},
    {"name": "Roronoa Zoro",       "role": "Swordsman",     "bounty": 1_111_000_000},
    {"name": "Nami",               "role": "Navigator",     "bounty":   366_000_000},
    {"name": "Usopp",              "role": "Sniper",        "bounty":   500_000_000},
    {"name": "Sanji",              "role": "Cook",          "bounty": 1_032_000_000},
    {"name": "Tony Tony Chopper",  "role": "Doctor",        "bounty":      1_000},
    {"name": "Nico Robin",         "role": "Archaeologist", "bounty":   930_000_000},
    {"name": "Franky",             "role": "Shipwright",    "bounty":   394_000_000},
    {"name": "Brook",              "role": "Musician",      "bounty":   383_000_000},
    {"name": "Jinbe",              "role": "Helmsman",      "bounty": 1_100_000_000},
]

BOUNTY_MULTIPLIERS = {"Captain": 1.5, "Swordsman": 1.2, "Cook": 1.1, "Helmsman": 1.15, "Archaeologist": 1.25}


def format_bounty(berry: int) -> str:
    return f"฿{berry:,}"


def bounty_after_rule(member: dict) -> int:
    mult = BOUNTY_MULTIPLIERS.get(member["role"], 1.0)
    return int(member["bounty"] * mult)


def total_crew_bounty(*members: dict, base: bool = True) -> int:
    if not members:
        return 0
    if base:
        return sum(m["bounty"] for m in members)
    return sum(bounty_after_rule(m) for m in members)


def describe_bounty(name: str, /, *, berry: int, **tags: str) -> str:
    parts = [f"{name}: {format_bounty(berry)}"]
    parts.extend(f"{k}={v}" for k, v in tags.items())
    return " | ".join(parts)


big_bounties = list(filter(lambda m: m["bounty"] > 500_000_000, CREW))
names_high = list(map(lambda m: m["name"], big_bounties))
sorted_crew = sorted(CREW, key=lambda m: m["bounty"], reverse=True)


@lru_cache(maxsize=None)
def crew_value_share(rank: int) -> int:
    if rank <= 1:
        return 1
    return rank + crew_value_share(rank - 1)


def bounty_posters(crew: list):
    for m in crew:
        yield f"WANTED: {m['name']} ({m['role']}) — {format_bounty(m['bounty'])}"


def log_bounty(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} → {result}")
        return result
    return wrapper


def pipe(*funcs):
    def applied(x):
        for f in funcs:
            x = f(x)
        return x
    return applied


def validate_crew(data):
    if not data:
        raise ValueError("Crew data is empty")
    return data


def enrich_stats(data):
    total = sum(m["bounty"] for m in data)
    for m in data:
        m["share_weight"] = round(m["bounty"] / total, 4)
    return data


def summarize(data):
    return {
        "total_bounty": format_bounty(sum(m["bounty"] for m in data)),
        "member_count": len(data),
        "top_earner": max(data, key=lambda m: m["bounty"])["name"],
    }


if __name__ == "__main__":
    print("=== One Piece Bounty System ===\n")

    luffy = CREW[0]
    print(f"Luffy's base: {format_bounty(luffy['bounty'])}")
    print(f"Luffy adjusted: {format_bounty(bounty_after_rule(luffy))}")
    print(f"Total base: {format_bounty(total_crew_bounty(*CREW))}")
    print(f"Adjusted total: {format_bounty(total_crew_bounty(*CREW, base=False))}")
    print(describe_bounty("Zoro", berry=1_111_000_000, style="wanted"))
    print(f"High bounties: {names_high}")
    print(f"Top earner: {sorted_crew[0]['name']}")
    print(f"Crew value contribution (rank 10): {crew_value_share(10)}")

    print("\nBounty posters:")
    for poster in bounty_posters(CREW[:3]):
        print(f"  {poster}")

    @log_bounty
    def lookup_bounty(name: str) -> str:
        for m in CREW:
            if m["name"] == name:
                return format_bounty(m["bounty"])
        return "Unknown"

    print(f"\nLookup: {lookup_bounty('Sanji')}")

    pipeline = pipe(validate_crew, enrich_stats, summarize)
    report = pipeline(CREW)
    print(f"\nCrew report: {report}")

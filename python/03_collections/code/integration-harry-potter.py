# Phase 03 Integration: Harry Potter — strings, lists, tuples, dicts, sets, nested data

from collections import defaultdict, Counter, namedtuple, deque
from typing import List, Dict, Tuple, Set

Spell = namedtuple("Spell", ["name", "level", "category"])

STUDENTS: List[Dict] = [
    {"name": "Harry Potter", "house": "Gryffindor", "year": 3, "patronus": "Stag", "friends": ["Ron", "Hermione"]},
    {"name": "Hermione Granger", "house": "Gryffindor", "year": 3, "patronus": "Otter", "friends": ["Harry", "Ron"]},
    {"name": "Ron Weasley", "house": "Gryffindor", "year": 3, "patronus": "Jack Russell Terrier", "friends": ["Harry", "Hermione"]},
    {"name": "Draco Malfoy", "house": "Slytherin", "year": 3, "patronus": None, "friends": ["Crabbe", "Goyle"]},
    {"name": "Luna Lovegood", "house": "Ravenclaw", "year": 2, "patronus": "Hare", "friends": ["Ginny"]},
    {"name": "Cedric Diggory", "house": "Hufflepuff", "year": 4, "patronus": "Badger", "friends": ["Cho"]},
]

SPELLS: List[Spell] = [
    Spell("Expelliarmus", 1, "Charm"),
    Spell("Lumos", 1, "Charm"),
    Spell("Accio", 2, "Charm"),
    Spell("Expecto Patronum", 3, "Defense"),
    Spell("Crucio", 4, "Dark Arts"),
    Spell("Avada Kedavra", 5, "Dark Arts"),
    Spell("Protego", 2, "Defense"),
    Spell("Wingardium Leviosa", 1, "Charm"),
]

PROFESSORS: Dict[str, Tuple[str, str]] = {
    "McGonagall": ("Transfiguration", "Gryffindor"),
    "Snape": ("Potions", "Slytherin"),
    "Flitwick": ("Charms", "Ravenclaw"),
    "Sprout": ("Herbology", "Hufflepuff"),
}

HOUSE_POINTS: Dict[str, int] = {"Gryffindor": 0, "Slytherin": 0, "Ravenclaw": 0, "Hufflepuff": 0}


def greet(hour: int) -> str:
    prefix = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    return f"\n{prefix} — Hogwarts Student Management System"


def list_students(students: List[Dict]) -> None:
    print(f"\nAll Students ({len(students)}):")
    for s in students:
        p = s["patronus"] or "None"
        print(f"  {s['name']:<22} | {s['house']:<12} | Yr {s['year']} | Patronus: {p}")


def find_by_house(students: List[Dict], house: str) -> List[str]:
    return [s["name"] for s in students if s["house"].lower() == house.lower()]


def top_students_by_year(students: List[Dict], year: int) -> List[str]:
    names = [s["name"].split()[0] for s in students if s["year"] == year]
    caps = [n.upper() for n in names]
    initials = [f"{s['name'].split()[0][0]}.{s['name'].split()[1][0]}." for s in students if s["year"] == year]
    return caps, initials


def castable_spells(level: int, spell_list: List[Spell], known_categories: Set[str]) -> List[str]:
    return [s.name for s in spell_list if s.level <= level and s.category in known_categories]


def tally_house_members(students: List[Dict]) -> Counter:
    return Counter(s["house"] for s in students)


def build_professor_by_house(professors: Dict[str, Tuple[str, str]]) -> Dict[str, str]:
    return {v[1]: k for k, v in professors.items()}


def award_points(house: str, points: int) -> None:
    HOUSE_POINTS[house] = HOUSE_POINTS.get(house, 0) + points


def show_professors(professors: Dict[str, Tuple[str, str]]) -> None:
    print("\nProfessors:")
    for name, (subject, house) in professors.items():
        print(f"  Prof. {name:<12} | {subject:<15} | {house}")


def main() -> None:
    print(greet(10))

    print("\n" + "=" * 55)
    list_students(STUDENTS)

    print(f"\nGryffindor students: {find_by_house(STUDENTS, 'Gryffindor')}")
    print(f"Slytherin students: {find_by_house(STUDENTS, 'Slytherin')}")

    caps, initials = top_students_by_year(STUDENTS, 3)
    print(f"\nYear 3 first names (upper): {caps}")
    print(f"Year 3 initials: {initials}")

    print(f"\nAvailable spells:")
    gryffindor_known = {"Charm", "Defense"}
    for s in castable_spells(3, SPELLS, gryffindor_known):
        print(f"  - {s}")

    print(f"\nHouse membership: {dict(tally_house_members(STUDENTS))}")

    prof_by_house = build_professor_by_house(PROFESSORS)
    print(f"Professor of Gryffindor: {prof_by_house.get('Gryffindor', 'Unknown')}")

    print(f"\nInitial house points: {HOUSE_POINTS}")
    award_points("Gryffindor", 50)
    award_points("Slytherin", 40)
    award_points("Ravenclaw", 35)
    award_points("Hufflepuff", 30)
    print(f"After Quidditch: {dict(HOUSE_POINTS)}")

    show_professors(PROFESSORS)

    print(f"\nAll unique houses: {set(s['house'] for s in STUDENTS)}")
    print(f"All unique patronuses: {set(s['patronus'] for s in STUDENTS if s['patronus'])}")

    recent_calls = deque(maxlen=3)
    recent_calls.append("list_students")
    recent_calls.append("find_by_house")
    recent_calls.append("award_points")
    recent_calls.append("show_professors")
    print(f"\nRecent function calls (deque): {list(recent_calls)}")

    house_heads = defaultdict(list)
    for name, (_, house) in PROFESSORS.items():
        house_heads[house].append(name)
    print(f"House heads (defaultdict): {dict(house_heads)}")

    category_counts = Counter(s.category for s in SPELLS)
    print(f"Spells by category: {dict(category_counts)}")

    named_students = [namedtuple("Student", ["name", "house"])(s["name"].split()[0], s["house"]) for s in STUDENTS[:3]]
    print(f"Named tuples: {[f'{s.name} ({s.house})' for s in named_students]}")


if __name__ == "__main__":
    main()

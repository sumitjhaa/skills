"""08-18-collections-abc-match-args.py — Custom Sequence, Mapping, pattern matching."""

from collections.abc import Sequence, Mapping, Iterable
from typing import Any


class ReadOnlyList(Sequence):
    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"ReadOnlyList({self._items})"


class ImmutableDict(Mapping):
    def __init__(self, **kwargs):
        self._data = dict(kwargs)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class Card:
    __match_args__ = ("rank", "suit")

    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"


def classify_card(card) -> str:
    match card:
        case Card("A", _):
            return "Ace"
        case Card(rank, "hearts") if rank in ("K", "Q", "J"):
            return f"Face of hearts"
        case Card(rank, suit):
            return f"{rank} of {suit}"
        case _:
            return "Unknown"


if __name__ == "__main__":
    rl = ReadOnlyList([10, 20, 30])
    print(f"Sequence: {list(rl)}, len={len(rl)}, is_sequence={isinstance(rl, Sequence)}")

    d = ImmutableDict(name="Bob", age=30)
    print(f"Mapping keys: {list(d.keys())}, age={d['age']}, is_mapping={isinstance(d, Mapping)}")

    print(f"Iterable check: {isinstance('hello', Iterable)}")

    print(classify_card(Card("A", "spades")))
    print(classify_card(Card("K", "hearts")))
    print(classify_card(Card("7", "clubs")))

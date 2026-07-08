"""04.28 Category theory: functors, natural transformations, monads."""
import numpy as np
from dataclasses import dataclass
from typing import Any, Callable

# Functor: List functor in Python
class ListFunctor:
    @staticmethod
    def fmap(f, xs):
        return [f(x) for x in xs]

print("List functor:", ListFunctor.fmap(lambda x: x**2, [1, 2, 3]))

# Functor: probability distribution monad
@dataclass
class Dist:
    values: np.ndarray
    probs: np.ndarray

    def normalize(self):
        self.probs = self.probs / self.probs.sum()
        return self

    def map(self, f):
        new_vals = np.array([f(v) for v in self.values])
        return Dist(new_vals, self.probs.copy())

    def flat_map(self, f):
        result = Dist(np.array([]), np.array([]))
        for v, p in zip(self.values, self.probs):
            d = f(v)
            d.probs *= p
            result = Dist(np.concatenate([result.values, d.values]),
                          np.concatenate([result.probs, d.probs]))
        return result.normalize()

# Distributions as a monad
fair_coin = Dist(np.array([0, 1]), np.array([0.5, 0.5]))
def biased_coin(x):
    return Dist(np.array([x, x+1]), np.array([0.7, 0.3]))

result = fair_coin.flat_map(biased_coin)
print(f"Monadic bind (fair coin -> biased): values={result.values}, probs={np.round(result.probs, 3)}")

# Natural transformation: list to set (deduplicate)
def list_to_set(xs):
    return list(dict.fromkeys(xs))

print(f"Natural transformation (list->set): {list_to_set([1, 2, 2, 3, 1, 3])}")

# Yoneda-like: hom-functor embedding
def hom_functor(X, all_objects):
    """Represent objects by their hom-sets."""
    return {Y: [f for f in [lambda x: x] if True] for Y in all_objects}

sets = hom_functor("A", ["A", "B"])
print(f"Yoneda embedding: Hom(A, -) has {len(sets)} targets")

# Product and coproduct
def categorical_product(a, b):
    return (a, b)

def categorical_coproduct(a, b):
    return ('either', a, b)

print(f"Product (1,2): {categorical_product(1, 2)}")
print(f"Coproduct: {categorical_coproduct(1, 2)}")

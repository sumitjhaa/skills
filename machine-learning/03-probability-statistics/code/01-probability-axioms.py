"""03.01 Probability Axioms: Verify Kolmogorov axioms for a dice example."""
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

Omega = {1, 2, 3, 4, 5, 6}
events = [
    set(), {1}, {2}, {3}, {4}, {5}, {6},
    {1, 3, 5}, {2, 4, 6}, Omega
]

def prob(ev):
    """Uniform probability measure."""
    return len(ev) / len(Omega)

print("=" * 60)
print("KOLMOGOROV AXIOMS VERIFICATION")
print("=" * 60)

print("\nAxiom 1: P(Ω) = 1")
print(f"  P(Ω) = {prob(Omega)}")
assert prob(Omega) == 1, "Axiom 1 failed!"

print("\nAxiom 2: P(A) ≥ 0 for all A ∈ F")
for e in events:
    p = prob(e)
    print(f"  P({e}) = {p:.2f}  {'✓' if p >= 0 else '✗'}")
all_nonneg = all(prob(e) >= 0 for e in events)
print(f"  All non-negative: {all_nonneg}")

print("\nAxiom 3: Countable additivity for disjoint events")
A = {1, 2}
B = {3, 5}
disjoint = A.isdisjoint(B)
p_A = prob(A)
p_B = prob(B)
p_union = prob(A | B)
print(f"  A = {A}, B = {B}, disjoint = {disjoint}")
print(f"  P(A) = {p_A:.2f}, P(B) = {p_B:.2f}")
print(f"  P(A∪B) = {p_union:.2f}")
print(f"  P(A) + P(B) = {p_A + p_B:.2f}")
print(f"  Additivity holds: {np.isclose(p_union, p_A + p_B)}")

print("\n" + "=" * 60)
print("SIGMA-ALGEBRA VERIFICATION")
print("=" * 60)
F = events
print(f"  Ω ∈ F: {Omega in F}")
all_complements = all({x for x in Omega if x not in e} in F for e in events)
print(f"  Closed under complement: {all_complements}")
all_unions = all(e1 | e2 in F for e1, e2 in combinations(events, 2))
print(f"  Closed under finite union: {all_unions}")

print("\n" + "=" * 60)
print("PROBABILITY RULES")
print("=" * 60)

print("\nComplement rule: P(A^c) = 1 - P(A)")
for e in events[:5]:
    e_c = Omega - e
    print(f"  P({e}^c) = {prob(e_c):.2f} = 1 - {prob(e):.2f}")
    assert np.isclose(prob(e_c), 1 - prob(e))

print("\nInclusion-Exclusion: P(A∪B) = P(A) + P(B) - P(A∩B)")
for e1, e2 in [(events[1], events[2]), (events[7], events[8])]:
    p_union_ie = prob(e1) + prob(e2) - prob(e1 & e2)
    print(f"  P({e1}∪{e2}) = {prob(e1 | e2):.2f} = {prob(e1)} + {prob(e2)} - {prob(e1 & e2)} = {p_union_ie:.2f}")
    assert np.isclose(prob(e1 | e2), p_union_ie)

print("\nMonotonicity: A ⊆ B ⇒ P(A) ≤ P(B)")
A_sub, B_sup = {1}, {1, 3, 5}
print(f"  {A_sub} ⊆ {B_sup}: P({A_sub}) = {prob(A_sub):.2f} ≤ P({B_sup}) = {prob(B_sup):.2f}")
assert prob(A_sub) <= prob(B_sup)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
events_subset = events[1:7]
labels = [f"{{{i}}}" for i in range(1, 7)]
probs = [prob(e) for e in events_subset]
colors = plt.cm.viridis(np.linspace(0.2, 0.8, 6))

axes[0].bar(labels, probs, color=colors)
axes[0].set_ylabel("Probability")
axes[0].set_title("Elementary Events P({i})")
axes[0].axhline(1/6, color='r', linestyle='--', label=f"1/6 = {1/6:.3f}")
axes[0].legend()
axes[0].grid(True, axis='y', alpha=0.3)

composite_events = ["Even", "Odd", "Ω"]
composite_probs = [prob({2,4,6}), prob({1,3,5}), prob(Omega)]
axes[1].bar(composite_events, composite_probs, color=['red', 'blue', 'green'])
axes[1].set_ylabel("Probability")
axes[1].set_title("Composite Events")
axes[1].grid(True, axis='y', alpha=0.3)

empty_events = ["P(∅)=0", "P(Ω)=1"]
empty_probs = [prob(set()), prob(Omega)]
axes[2].bar(empty_events, empty_probs, color=['gray', 'green'])
axes[2].set_ylabel("Probability")
axes[2].set_title("Boundary Conditions")
axes[2].grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/01-probability-axioms.png")
plt.close()
print("\nAxiom verification plot saved.")

all_axioms = (prob(Omega) == 1 and all_nonneg and
              np.isclose(prob(A | B), prob(A) + prob(B)))
print(f"\nAll probability axioms satisfied: {all_axioms}")

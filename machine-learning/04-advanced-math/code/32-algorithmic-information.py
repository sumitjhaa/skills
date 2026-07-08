"""04.32 Algorithmic information theory: Kolmogorov complexity approximation."""
import numpy as np
import zlib
import math

def kolmogorov_approx(s):
    return len(zlib.compress(s.encode()))

# Compare random vs. structured strings
strings = {
    "constant": "A" * 1000,
    "fibonacci": "0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987",
    "random": ''.join(np.random.choice(list("ABCDEFGH"), 500)),
    "repeating": "abc" * 333 + "a",
    "pi_digits": "31415926535897932384626433832795028841971693993751",
}
print("Kolmogorov complexity estimates (compressed length in bytes):")
for name, s in strings.items():
    kc = kolmogorov_approx(s)
    print(f"  {name:12s}: {kc:4d} bytes (len={len(s)})")

# Algorithmic probability: Solomonoff induction simulation
def solomonoff_predict(sequence, alphabet=['0', '1']):
    """Simple prediction using Bayes (approximation via counts)."""
    n = len(sequence)
    counts = {}
    for i in range(n - 1):
        prefix = sequence[:i+1]
        suffix = sequence[i+1]
        if prefix not in counts:
            counts[prefix] = {}
        counts[prefix][suffix] = counts[prefix].get(suffix, 0) + 1
    # Predict next symbol
    if sequence in counts:
        next_counts = counts[sequence]
        total = sum(next_counts.values())
        probs = {s: c/total for s, c in next_counts.items()}
        return probs
    return {s: 1/len(alphabet) for s in alphabet}

seq = "0101010101"
probs = solomonoff_predict(seq)
print(f"\nSolomonoff-style prediction for '{seq}' next symbol:")
for s, p in probs.items():
    print(f"  P('{s}') = {p:.4f}")

# Levin's universal search: compute shortest program approximately
def universal_search(target, max_len=8):
    """Brute-force search for program generating target (toy)."""
    for length in range(1, max_len + 1):
        for prog_bits in range(2**length):
            prog = format(prog_bits, f'0{length}b')
            if run_program(prog) == target:
                return prog
    return None

def run_program(bits):
    """Toy program interpreter: treats bits as instructions."""
    if len(bits) >= 4 and bits[:4] == "0110":
        n = int(bits[4:], 2) if len(bits) > 4 else 0
        return "A" * (n + 1)
    return None

print(f"\nUniversal search for 'AAAA': {universal_search('AAAA', 8)}")

"""DNA sequence analysis — extracting codons with indexing and slicing"""

dna = "ATGCGTACGTTAG"

print(f"DNA Sequence: {dna}")
print(f"Length: {len(dna)} bases")

print("\n=== Single Base Access ===")
print(f"  First base (index 0): {dna[0]}")
print(f"  Last base (index -1): {dna[-1]}")
print(f"  Third base (index 2): {dna[2]}")

print("\n=== Codon Extraction ===")
print(f"  First codon [0:3]: {dna[0:3]}")
print(f"  Second codon [3:6]: {dna[3:6]}")
print(f"  Third codon [6:9]: {dna[6:9]}")

print("\n=== Slice Shorthand ===")
print(f"  First 4 bases [:4]: {dna[:4]}")
print(f"  From base 4 onward [4:]: {dna[4:]}")
print(f"  Last 3 bases [-3:]: {dna[-3:]}")

print("\n=== Stepping ===")
print(f"  Every 2nd base [::2]: {dna[::2]}")
print(f"  Every 3rd base [::3]: {dna[::3]}")
print(f"  Reversed [::-1]: {dna[::-1]}")
print(f"  Reverse every 2nd [::-2]: {dna[::-2]}")

print("\n=== Immutability ===")
print("  Strings cannot be modified in place.")
print("  dna[0] = 'T' would raise TypeError.")

"""Association Rules (Apriori) from scratch."""
import numpy as np
from itertools import combinations

class Apriori:
    def __init__(self, min_support=0.3, min_confidence=0.7):
        self.min_support = min_support
        self.min_confidence = min_confidence

    def fit(self, transactions):
        self.transactions = transactions
        n = len(transactions)
        items = set()
        for t in transactions: items.update(t)
        items = sorted(items)

        freq_sets = {}
        k = 1
        candidates = {frozenset([i]) for i in items}
        while candidates:
            freq = {}
            for c in candidates:
                support = sum(1 for t in transactions if c.issubset(t)) / n
                if support >= self.min_support:
                    freq[c] = support
            freq_sets.update(freq)

            k += 1
            candidates = set()
            freq_list = list(freq.keys())
            for i in range(len(freq_list)):
                for j in range(i+1, len(freq_list)):
                    union = freq_list[i] | freq_list[j]
                    if len(union) == k:
                        valid = True
                        for subset in combinations(union, k-1):
                            if frozenset(subset) not in freq:
                                valid = False; break
                        if valid:
                            candidates.add(union)

        self.frequent_itemsets_ = freq_sets
        self.rules_ = self._generate_rules()
        return self

    def _generate_rules(self):
        rules = []
        for itemset, support in self.frequent_itemsets_.items():
            if len(itemset) < 2: continue
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    if not consequent: continue
                    conf = support / self.frequent_itemsets_.get(antecedent, 0)
                    if conf >= self.min_confidence:
                        lift = conf / self.frequent_itemsets_.get(consequent, 0)
                        rules.append((antecedent, consequent, support, conf, lift))
        return sorted(rules, key=lambda r: r[4], reverse=True)

    def print_rules(self, n=10):
        print(f"Top {n} association rules:")
        for ant, con, sup, conf, lift in self.rules_[:n]:
            print(f"  {set(ant)} -> {set(con)}  (supp={sup:.2f}, conf={conf:.2f}, lift={lift:.2f})")

if __name__ == "__main__":
    transactions = [
        {'milk', 'bread', 'eggs'},
        {'milk', 'bread'},
        {'milk', 'eggs'},
        {'bread', 'eggs', 'butter'},
        {'milk', 'bread', 'eggs', 'butter'},
        {'eggs', 'butter'},
        {'milk', 'butter'},
        {'bread', 'butter'},
        {'milk', 'bread', 'butter'},
        {'eggs', 'bread', 'milk'},
    ]

    ap = Apriori(min_support=0.3, min_confidence=0.6)
    ap.fit(transactions)
    ap.print_rules(n=5)

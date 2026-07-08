"""
09.01 Text Processing — Porter Stemmer & Lemmatizer
Built with only numpy, scipy, matplotlib.
"""
import re
import numpy as np


# ── Porter Stemmer (simplified) ──────────────────────────────────────────────

class PorterStemmer:
    """Minimal Porter stemmer implementing key rules."""

    def __init__(self):
        self.vowels = "aeiou"

    def _is_consonant(self, word, i):
        if word[i] in self.vowels:
            return False
        if word[i] == 'y' and i > 0 and self._is_consonant(word, i - 1):
            return False
        return True

    def _measure(self, word):
        """Compute m — VC count."""
        n = len(word)
        m = 0
        i = 0
        while i < n - 1:
            if not self._is_consonant(word, i) and self._is_consonant(word, i + 1):
                m += 1
                i += 1
            i += 1
        return m

    def _has_vowel(self, word):
        return any(c in self.vowels for c in word)

    def _double_c(self, word):
        n = len(word)
        if n < 2:
            return False
        return (self._is_consonant(word, n - 1) and
                self._is_consonant(word, n - 2) and
                word[n - 1] == word[n - 2])

    def _step1a(self, word):
        if word.endswith("sses"):
            return word[:-2]
        if word.endswith("ies"):
            return word[:-2]
        if word.endswith("ss"):
            return word
        if word.endswith("s"):
            # ... more complex in real impl
            return word[:-1]
        return word

    def stem(self, word):
        word = word.lower()
        if len(word) <= 2:
            return word
        word = self._step1a(word)
        # Simplified — real Porter has 5 steps
        return word


# ── Simple Lemmatizer (WordNet-style lookup) ────────────────────────────────

class SimpleLemmatizer:
    """Lookup-based lemmatizer with basic inflection rules."""

    def __init__(self):
        self.lemma_table = {
            "running": "run", "runs": "run", "ran": "run",
            "better": "good", "best": "good",
            "went": "go", "goes": "go", "going": "go",
            "mice": "mouse", "children": "child",
            "wolves": "wolf", "knives": "knife",
            "took": "take", "taken": "take", "taking": "take",
            "eating": "eat", "eats": "eat", "ate": "eat",
            "said": "say", "says": "say",
            "made": "make", "making": "make",
            "did": "do", "does": "do", "done": "do",
            "bought": "buy", "buying": "buy",
            "thought": "think", "thinks": "think", "thinking": "think",
            "came": "come", "comes": "come", "coming": "come",
            "gave": "give", "gives": "give", "giving": "give",
            "wrote": "write", "writes": "write", "writing": "write",
            "sang": "sing", "sung": "sing",
            "sat": "sit", "sits": "sit",
            "men": "man", "women": "woman",
            "feet": "foot", "teeth": "tooth",
            "froze": "freeze", "frozen": "freeze",
            "chose": "choose", "chosen": "choose",
        }

    def lemmatize(self, word, pos="n"):
        """Return lemma. pos: n= noun, v= verb, a= adjective."""
        word = word.lower()
        if word in self.lemma_table:
            return self.lemma_table[word]
        # Basic rules: -s -> - (cats->cat), -ed -> - (walked->walk), -ing -> - (running->run)
        if word.endswith("ies") and len(word) > 4:
            return word[:-3] + "y"
        if word.endswith("ves"):
            return word[:-3] + "f"
        if word.endswith("es") and word.endswith(("sses", "shes", "ches", "xes", "zes")):
            return word[:-2]
        if word.endswith("s") and not word.endswith("ss"):
            return word[:-1]
        if pos == "v" and word.endswith("ed"):
            return word[:-2] if word[-3] in "aeiou" else word[:-1]
        if pos == "v" and word.endswith("ing"):
            return word[:-3] + "e" if len(word) > 5 else word[:-3]
        return word


def normalize(text):
    """Basic text normalization pipeline."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


if __name__ == "__main__":
    stemmer = PorterStemmer()
    lemmatizer = SimpleLemmatizer()

    text = "The running children ate better meals and went to the store"
    tokens = normalize(text).split()
    print(f"{'word':<12} {'stem':<12} {'lemma':<12}")
    print("-" * 36)
    for t in tokens:
        s = stemmer.stem(t)
        l = lemmatizer.lemmatize(t)
        print(f"{t:<12} {s:<12} {l:<12}")

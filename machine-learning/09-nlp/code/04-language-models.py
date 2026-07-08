"""
09.04 Language Models — N-gram LM with Kneser-Ney Smoothing
Built with only numpy, scipy, matplotlib.
"""
from collections import defaultdict, Counter
import math


class NGramLM:
    """N-gram language model with Kneser-Ney smoothing."""

    def __init__(self, n=3, discount=0.75):
        self.n = n
        self.discount = discount
        self.ngrams = defaultdict(Counter)
        self.context_counts = Counter()
        self.vocab = set()
        self.vocab_size = 0

    def fit(self, corpus):
        for sentence in corpus:
            tokens = sentence.lower().split()
            tokens = ["<s>"] * (self.n - 1) + tokens + ["</s>"]
            self.vocab.update(tokens)
            for i in range(len(tokens) - self.n + 1):
                context = tuple(tokens[i:i + self.n - 1])
                word = tokens[i + self.n - 1]
                self.ngrams[context][word] += 1
                self.context_counts[context] += 1
        self.vocab_size = len(self.vocab)

    def _continuation_counts(self):
        """Count how many unique contexts each word appears in (for Kneser-Ney)."""
        word_contexts = Counter()
        for context, counter in self.ngrams.items():
            for word in counter:
                word_contexts[word] += 1
        return word_contexts

    def _total_continuations(self, word_contexts):
        return sum(word_contexts.values())

    def probability(self, word, context):
        """P(word | context) with Kneser-Ney smoothing."""
        context = tuple(context)
        count = self.ngrams.get(context, {}).get(word, 0)
        context_total = self.context_counts.get(context, 0)

        # Higher-order probability with discount
        if context_total > 0:
            higher = max(count - self.discount, 0) / context_total
        else:
            higher = 0.0

        # Backoff weight
        if context_total > 0:
            num_distinct = len(self.ngrams.get(context, {}))
            backoff_weight = (self.discount * num_distinct) / context_total
        else:
            backoff_weight = 1.0

        # Lower-order probability (Kneser-Ney continuation)
        word_contexts = self._continuation_counts()
        total_cont = self._total_continuations(word_contexts)
        if total_cont > 0:
            lower = word_contexts.get(word, 0) / total_cont
        else:
            lower = 1.0 / self.vocab_size

        return higher + backoff_weight * lower

    def sentence_log_prob(self, sentence):
        tokens = sentence.lower().split()
        tokens = ["<s>"] * (self.n - 1) + tokens + ["</s>"]
        log_prob = 0.0
        for i in range(self.n - 1, len(tokens)):
            context = tokens[i - self.n + 1:i]
            word = tokens[i]
            p = self.probability(word, context)
            log_prob += math.log2(p) if p > 0 else -float("inf")
        return log_prob

    def perplexity(self, corpus):
        total_log_prob = 0.0
        total_tokens = 0
        for sentence in corpus:
            log_prob = self.sentence_log_prob(sentence)
            tokens = sentence.lower().split()
            total_log_prob += log_prob
            total_tokens += len(tokens) + 1
        return 2 ** (-total_log_prob / total_tokens)

    def generate(self, context, max_len=10):
        context = list(context)
        output = list(context)
        for _ in range(max_len):
            ctx = tuple(context[-(self.n - 1):]) if len(context) >= self.n - 1 else tuple(["<s>"] * (self.n - 1 - len(context)) + context)
            candidates = self.ngrams.get(ctx, {})
            if not candidates:
                # Fallback to uniform
                import random
                word = random.choice(list(self.vocab - {"<s>", "</s>"}))
            else:
                total = sum(candidates.values())
                import random
                r = random.random() * total
                cumulative = 0
                word = None
                for w, c in candidates.items():
                    cumulative += c
                    if r <= cumulative:
                        word = w
                        break
            if word in ("</s>", None):
                break
            output.append(word)
            context.append(word)
        return " ".join(output)


if __name__ == "__main__":
    corpus = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "a cat is on the mat near the log",
        "the mat is soft and the log is hard",
        "i sat on a mat near a cat",
        "the dog and the cat are friends",
    ]
    lm = NGramLM(n=3, discount=0.75)
    lm.fit(corpus)

    test = ["the cat sat on the log", "a dog is on the mat"]
    for t in test:
        lp = lm.sentence_log_prob(t)
        ppl = 2 ** (-lp / (len(t.split()) + 1))
        print(f"Sentence: '{t}'")
        print(f"  Log-prob: {lp:.2f}, Perplexity: {ppl:.2f}")

    print(f"\nCorpus perplexity: {lm.perplexity(corpus):.2f}")
    print(f"\nGenerated: {lm.generate(['the', 'cat'], max_len=8)}")

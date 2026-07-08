# 09.02 Tokenisation

## Learning Objectives
- Understand word, subword, and character tokenisation
- Implement BPE (Byte-Pair Encoding) tokeniser
- Apply WordPiece and Unigram tokenisation
- Compare tokenisation algorithms for different languages

## Word Tokenisation

### Whitespace Tokenisation
```python
tokens = text.split()  # simple but fails on punctuation, contractions
```

### Treebank Tokenizer (NLTK)
Handles contractions and punctuation:

```python
from nltk.tokenize import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()
tokenizer.tokenize("I'm going to the U.S.")
# → ["I", "'m", "going", "to", "the", "U.S.", "."]
```

## Subword Tokenisation

### Byte-Pair Encoding (BPE)

**Algorithm**:
1. Start with character vocabulary
2. Count all adjacent token pairs
3. Merge most frequent pair → new token
4. Repeat until vocabulary size reached

```python
# Base vocabulary
"l o w <w> l o w e r <w> n e w e s t <w> w i d e s t <w>"

# After merges:
# 1. "e" + "s" → "es" (most frequent)
# 2. "es" + "t" → "est"
# 3. "l" + "o" → "lo"
# 4. "lo" + "w" → "low"
```

**GPT-2 uses BPE** with 50,257 tokens, handling bytes directly (byte-level BPE).

### WordPiece

**Algorithm**:
1. Start with character vocabulary
2. Score each pair: $\text{score}(a, b) = \frac{\text{freq}(ab)}{\text{freq}(a) \cdot \text{freq}(b)}$
3. Merge highest-scoring pair
4. Repeat until vocabulary size reached

**BERT uses WordPiece** with 30,000 tokens.

### Unigram (SentencePiece)

**Algorithm**:
1. Start with large vocabulary (all possible subwords)
2. Compute loss for current vocabulary
3. Remove tokens that increase loss least
4. Repeat until target vocabulary size

**T5/XLNet uses Unigram** via SentencePiece with 32,000 tokens.

## SentencePiece

Language-agnostic tokenisation:

```python
import sentencepiece as spm

# Train
spm.SentencePieceTrainer.train(
    input='corpus.txt',
    model_prefix='m',
    vocab_size=32000,
    character_coverage=1.0,
    model_type='unigram'  # or 'bpe'
)

# Load and use
sp = spm.SentencePieceProcessor(model_file='m.model')
sp.encode("Hello world")  # → [151, 102, 1002]
sp.decode([151, 102, 1002])  # → "Hello world"
```

## Character Tokenisation

### Advantages
- No unknown tokens
- Language-agnostic
- Small vocabulary (~100-200)

### Disadvantages
- Long sequences (5×+ longer than subword)
- Harder to learn linguistic structure

## Comparison

| Method | Vocabulary | Example: "unhappiness" | Model |
|--------|-----------|----------------------|-------|
| Word | 500K+ | "unhappiness" | GloVe |
| BPE | 50K | "un", "happiness" | GPT-2 |
| WordPiece | 30K | "un", "##happiness" | BERT |
| Unigram | 32K | "un", "happiness" | T5 |
| Character | ~100 | "u", "n", "h", "a", ... | CharCNN |

## Special Tokens

### BERT
```
[CLS] = 101   [SEP] = 102   [PAD] = 0
[UNK] = 100   [MASK] = 103
```

### GPT-2
```
<s> = 50256   <|endoftext|> = 50256
```

## Practical Considerations
- **Pretokenisation**: BPE/WordPiece typically run on whitespace-tokenised words
- **Unknown tokens**: BPE can always fall back to bytes; WordPiece produces [UNK]
- **Language-specific**: Korean/Japanese benefit from SentencePiece (no spaces)
- **Vocabulary size**: 30K-50K for BERT/GPT; 250K for RoBERTa (larger vocab, same subwords)

## References
- Sennrich, Haddow, Birch, "Neural Machine Translation of Rare Words with Subword Units", ACL 2016
- Wu, Schuster, et al., "Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation (WordPiece)", 2016
- Kudo & Richardson, "SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing", EMNLP 2018
- Kudo, "Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates", ACL 2018

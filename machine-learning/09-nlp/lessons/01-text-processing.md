# 09.01 Text Processing

## Learning Objectives
- Understand text cleaning and normalisation pipelines
- Implement regular expressions for text preprocessing
- Apply Unicode normalisation and stemming/lemmatisation
- Build efficient tokenisation with spaCy and NLTK

## Text Cleaning

### Lowercasing
```python
text = text.lower()  # reduces vocabulary size, loses case information
```

### Removing Special Characters
```python
import re
text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # keep alphanumeric + spaces
```

### Whitespace Normalisation
```python
text = re.sub(r'\s+', ' ', text).strip()  # collapse multiple spaces
```

## Unicode Normalisation

### NFC vs NFD vs NFKC vs NFKD
| Form | Description | Use Case |
|------|-------------|----------|
| NFC | Canonical composition | Default for storage |
| NFD | Canonical decomposition | Comparing characters |
| NFKC | Compatibility composition | Removing formatting |
| NFKD | Compatibility decomposition | Lenient matching |

```python
import unicodedata
text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
```

## Regular Expressions

### Common Patterns
```python
# Email
r'[\w\.-]+@[\w\.-]+\.\w+'

# URL
r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

# Hashtags
r'#\w+'

# Mentions
r'@\w+'

# Numbers (including decimals)
r'-?\d+(?:\.\d+)?'

# Dates (YYYY-MM-DD)
r'\d{4}-\d{2}-\d{2}'
```

## Stemming & Lemmatisation

### Stemming
Rule-based truncation to root form:

```python
from nltk.stem import PorterStemmer
ps = PorterStemmer()
ps.stem("running")   # → "run"
ps.stem("studies")   # → "studi" (over-stems)
```

### Lemmatisation
Vocabulary-aware reduction to dictionary form:

```python
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize("running", "v")  # → "run"
lemmatizer.lemmatize("studies", "n")  # → "study"
```

## Language Detection

```python
from langdetect import detect
detect("Hello world")       # → "en"
detect("Bonjour le monde")  # → "fr"
```

## Code: Text Processing Pipeline

```python
import re
import unicodedata

def clean_text(text, lower=True, remove_punct=True, normalize_unicode=True):
    if normalize_unicode:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    if lower:
        text = text.lower()
    if remove_punct:
        text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_sentence(text, model='spacy'):
    import spacy
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

def process_document(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return clean_text(text)
```

## Reference Resources
- NLTK documentation: https://www.nltk.org/
- spaCy 101: https://spacy.io/usage/spacy-101
- Unicode Standard Annex #15: Unicode Normalisation Forms
- Regex101: https://regex101.com/

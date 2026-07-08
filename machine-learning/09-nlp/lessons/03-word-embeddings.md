# 09.03 Word Embeddings

## Learning Objectives
- Understand distributional semantics hypothesis
- Implement Word2Vec (CBOW and Skip-gram)
- Apply GloVe and FastText for pretrained embeddings
- Evaluate embeddings with word analogy tasks

## Distributional Semantics

"You shall know a word by the company it keeps" — Firth (1957)

Words with similar contexts have similar meanings.

## Word2Vec

### CBOW (Continuous Bag of Words)
Predict target word from context:

$$p(w_t | w_{t-2}, w_{t-1}, w_{t+1}, w_{t+2}) = \text{softmax}(W \cdot \bar{v})$$

- $\bar{v} = \frac{1}{C} \sum_{c} v_c$ (average context embeddings)
- Efficient: trains faster than Skip-gram for frequent words

### Skip-gram
Predict context words from target:

$$p(w_{t+j} | w_t) = \text{softmax}(v_{w_t}^\top u_{w_{t+j}})$$

- Better for rare words
- Hierarchical softmax or negative sampling for efficiency

### Negative Sampling
$$p(D = 1 | w, c) = \sigma(v_w^\top v_c)$$
$$p(D = 0 | w, c) = 1 - \sigma(v_w^\top v_c)$$

Loss: $$\mathcal{L} = -\log\sigma(v_{w_t}^\top v_c) - \sum_{k=1}^K \log\sigma(-v_{w_t}^\top v_{c_k})$$

## GloVe (Global Vectors)

### Co-occurrence Matrix
$X_{ij}$: count of word $i$ appearing with word $j$ in a window.

### Objective
$$\mathcal{L} = \sum_{i,j} f(X_{ij}) (w_i^\top \tilde{w}_j + b_i + \tilde{b}_j - \log X_{ij})^2$$

- $f(X_{ij})$: weighting function (clips rare/very frequent pairs)
- Count-based + prediction-based hybrid

## FastText

### Subword Information
Each word = bag of character n-grams (3-6 grams):

$$v_{\text{apple}} = \sum_{g \in \text{ngrams(apple)}} v_g$$

- Handles out-of-vocabulary words
- Better for morphologically rich languages

## Code: Word2Vec with Negative Sampling

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class Word2Vec(nn.Module):
    def __init__(self, vocab_size, embedding_dim=100, noise_dist=None):
        super().__init__()
        self.v_embed = nn.Embedding(vocab_size, embedding_dim)
        self.u_embed = nn.Embedding(vocab_size, embedding_dim)

    def forward(self, target_words, context_words, noise_words):
        # Positive samples
        v_target = self.v_embed(target_words)
        u_context = self.u_embed(context_words)
        pos_score = (v_target * u_context).sum(dim=1)
        pos_loss = F.logsigmoid(pos_score)
        
        # Negative samples
        v_target_exp = v_target.unsqueeze(1).expand(-1, noise_words.size(1), -1)
        u_noise = self.u_embed(noise_words)
        neg_score = (v_target_exp * u_noise).sum(dim=2)
        neg_loss = F.logsigmoid(-neg_score).sum(dim=1)
        
        return -(pos_loss + neg_loss).mean()
```

## Evaluation: Word Analogies

### Semantic
- `king - man + woman = queen`
- `France - Paris + Tokyo = Japan`

### Syntactic
- `run - ran + walked = walk`
- `big - bigger + smaller = small`

### 3CosAdd
$$v_{\text{target}} = \arg\max_{v \in V} \cos(v, v_b - v_a + v_c)$$

## Benchmarks

| Embedding | Corpus | Dim | Wordsim-353 | Google Analogy |
|-----------|--------|-----|-------------|----------------|
| Word2Vec (Google) | Google News 100B | 300 | 68.4% | 74.2% |
| GloVe (Common Crawl) | 42B tokens | 300 | 67.2% | 76.9% |
| FastText (Common Crawl) | 600B tokens | 300 | 71.5% | 80.1% |
| BERT (contextual) | Books + Wikipedia | 768 | — | — |

## Limitations
- **Static embeddings**: Same representation for each word regardless of context
- **Polysemy**: "bank" (river vs financial) uses one vector
- **OOV**: Word2Vec/GloVe cannot handle unseen words
- **Bias**: Embeddings encode gender/racial biases from training data

## References
- Mikolov, Chen, Corrado, Dean, "Efficient Estimation of Word Representations in Vector Space", ICLR 2013
- Mikolov, Sutskever, Chen, Corrado, Dean, "Distributed Representations of Words and Phrases and their Compositionality", NeurIPS 2013
- Pennington, Socher, Manning, "GloVe: Global Vectors for Word Representation", EMNLP 2014
- Bojanowski, Grave, Joulin, Mikolov, "Enriching Word Vectors with Subword Information (FastText)", TACL 2017

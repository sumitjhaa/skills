"""
12.06: Full RAG System with Evaluation
Retrieval-Augmented Generation with document ingestion,
embedding, retrieval, generation, and evaluation metrics.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Dict
import re


# ─────────────────────────────────────────────
# Document loading and chunking
# ─────────────────────────────────────────────

DOCUMENTS = [
    "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves.",
    "Deep learning is a subset of machine learning that uses neural networks with many layers (deep neural networks) to model and understand complex patterns. It has revolutionized fields like computer vision, natural language processing, and speech recognition.",
    "Neural networks are computing systems inspired by biological neural networks in the human brain. They consist of interconnected nodes (neurons) organized in layers that process information using connectionist approaches to computation.",
    "Supervised learning is a type of machine learning where the model is trained on labeled data. The algorithm learns to map inputs to outputs based on example input-output pairs provided in the training data.",
    "Unsupervised learning is a type of machine learning where the model finds patterns in unlabeled data. Common techniques include clustering, dimensionality reduction, and density estimation.",
    "Reinforcement learning is a type of machine learning where an agent learns to make decisions by interacting with an environment. The agent receives rewards or penalties based on its actions and learns to maximize cumulative reward.",
    "Natural language processing (NLP) is a branch of AI that helps computers understand, interpret, and manipulate human language. NLP combines computational linguistics with statistical and machine learning models.",
    "Computer vision is a field of AI that enables computers to derive meaningful information from digital images, videos, and other visual inputs. It works on automating tasks that the human visual system can perform.",
    "Transfer learning is a machine learning technique where a model developed for one task is reused as the starting point for a model on a second task. It is popular in deep learning where pre-trained models are used as the starting point.",
    "Gradient descent is an optimization algorithm used to minimize the loss function in machine learning models. It iteratively adjusts model parameters in the direction of steepest descent of the loss function.",
    "Backpropagation is the primary algorithm for training neural networks. It computes the gradient of the loss function with respect to each weight by applying the chain rule, working backwards from the output layer.",
    "Transformers are a neural network architecture that uses self-attention mechanisms to process sequential data. They have become the dominant architecture in NLP and are increasingly used in computer vision and other domains.",
    "Convolutional neural networks (CNNs) are a class of deep neural networks designed for processing structured grid data like images. They use convolutional layers that apply filters to detect features at different spatial hierarchies.",
    "Recurrent neural networks (RNNs) are a class of neural networks designed for processing sequential data. They maintain a hidden state that captures information about previous inputs in the sequence.",
    "Attention mechanisms allow neural networks to focus on relevant parts of the input when producing output. The key innovation of transformers is the self-attention mechanism that weighs the importance of different elements in a sequence.",
    "Generative adversarial networks (GANs) consist of two neural networks, a generator and a discriminator, that compete against each other. The generator creates fake data while the discriminator tries to distinguish real from fake.",
    "Autoencoders are neural networks that learn efficient data representations (encodings) by training to reconstruct their input. They consist of an encoder that compresses the input and a decoder that reconstructs it.",
    "Regularization techniques prevent overfitting in machine learning models. Common methods include L1/L2 regularization, dropout, early stopping, and data augmentation.",
    "Hyperparameter tuning is the process of finding the optimal set of hyperparameters for a machine learning model. Methods include grid search, random search, and Bayesian optimization.",
    "Ensemble methods combine multiple machine learning models to produce better predictive performance than any single model. Popular ensemble techniques include bagging, boosting, and stacking.",
]


def chunk_document(text: str, chunk_size: int = 128, overlap: int = 32) -> List[Dict]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text = ' '.join(words[start:end])
        chunks.append({
            'text': chunk_text,
            'start': start,
            'end': end,
        })
        if end >= len(words):
            break
        start = end - overlap
    return chunks


def load_and_chunk_all(docs: List[str], chunk_size: int = 64, overlap: int = 16) -> List[Dict]:
    """Load and chunk all documents."""
    all_chunks = []
    for i, doc in enumerate(docs):
        chunks = chunk_document(doc, chunk_size, overlap)
        for chunk in chunks:
            chunk['doc_id'] = i
        all_chunks.extend(chunks)
    return all_chunks


# ─────────────────────────────────────────────
# Embedding (simple TF-IDF-like)
# ─────────────────────────────────────────────

def tokenize(text: str) -> List[str]:
    """Simple tokenizer: lowercase + split on non-alphanumeric."""
    return re.findall(r'\b[a-z]+\b', text.lower())


def build_vocab(chunks: List[Dict]) -> Dict[str, int]:
    vocab = {}
    for chunk in chunks:
        for token in tokenize(chunk['text']):
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab


def compute_tfidf(text: str, vocab: Dict, idf: Optional[Dict[str, float]] = None) -> np.ndarray:
    tokens = tokenize(text)
    vec = np.zeros(len(vocab), dtype=np.float64)
    for token in tokens:
        if token in vocab:
            vec[vocab[token]] += 1.0
    if vec.sum() > 0:
        vec = vec / vec.sum()  # TF normalization
    if idf is not None:
        for token in tokens:
            if token in idf:
                vec[vocab[token]] *= idf[token]
    return vec


def compute_idf(chunks: List[Dict], vocab: Dict) -> Dict[str, float]:
    N = len(chunks)
    doc_freq = {token: 0 for token in vocab}
    for chunk in chunks:
        tokens = set(tokenize(chunk['text']))
        for token in tokens:
            if token in doc_freq:
                doc_freq[token] += 1
    return {token: np.log(N / (1 + freq)) for token, freq in doc_freq.items()}


def embed_chunks(chunks: List[Dict], vocab: Dict, idf: Dict) -> np.ndarray:
    embeddings = []
    for chunk in chunks:
        vec = compute_tfidf(chunk['text'], vocab, idf)
        # L2 normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        embeddings.append(vec)
    return np.stack(embeddings)


# ─────────────────────────────────────────────
# Vector store
# ─────────────────────────────────────────────

class VectorStore:
    def __init__(self):
        self.embeddings: Optional[np.ndarray] = None
        self.chunks: List[Dict] = []

    def add(self, chunks: List[Dict], embeddings: np.ndarray):
        self.chunks = chunks
        self.embeddings = embeddings

    def search(self, query_vec: np.ndarray, k: int = 5) -> List[Tuple[Dict, float]]:
        if self.embeddings is None:
            return []
        scores = self.embeddings @ query_vec  # cosine (vectors are normalized)
        top_indices = np.argsort(scores)[-k:][::-1]
        results = []
        for idx in top_indices:
            results.append((self.chunks[idx], float(scores[idx])))
        return results


# ─────────────────────────────────────────────
# Generator (simple template-based)
# ─────────────────────────────────────────────

class SimpleGenerator:
    """A template-based generator for demonstration purposes."""
    def generate(self, query: str, context: str) -> str:
        # Simple extractive + template generation
        context_sentences = context.split('.')
        relevant = [s.strip() for s in context_sentences if len(s.strip()) > 10]
        if not relevant:
            return f"Based on my knowledge, I can tell you that {query} relates to machine learning concepts."

        # Pick most relevant sentence (contains query terms)
        query_terms = set(tokenize(query))
        best_sentence = relevant[0]
        best_score = 0
        for sent in relevant:
            sent_terms = set(tokenize(sent))
            overlap = len(query_terms & sent_terms)
            if overlap > best_score:
                best_score = overlap
                best_sentence = sent

        return f"Based on the available information: {best_sentence}."


# ─────────────────────────────────────────────
# Synthetic QA pairs for evaluation
# ─────────────────────────────────────────────

QA_PAIRS = [
    ("What is machine learning?",
     "subset of artificial intelligence that enables systems to learn"),
    ("What is deep learning?",
     "uses neural networks with many layers"),
    ("How do neural networks work?",
     "interconnected nodes organized in layers"),
    ("What is supervised learning?",
     "trained on labeled data"),
    ("What is unsupervised learning?",
     "finds patterns in unlabeled data"),
    ("What is reinforcement learning?",
     "learns to make decisions by interacting with environment"),
    ("What is NLP?",
     "computers understand human language"),
    ("What is computer vision?",
     "interpret visual information"),
    ("What is transfer learning?",
     "reused as starting point for second task"),
    ("What is gradient descent?",
     "optimization algorithm to minimize loss function"),
    ("What is backpropagation?",
     "computes gradient of loss function with respect to weights"),
    ("What are transformers?",
     "self-attention mechanisms to process sequential data"),
    ("What are CNNs?",
     "convolutional layers that detect features"),
    ("What are RNNs?",
     "processing sequential data maintaining hidden state"),
    ("What is attention?",
     "focus on relevant parts of input"),
]


# ─────────────────────────────────────────────
# Evaluation metrics
# ─────────────────────────────────────────────

def recall_at_k(retrieved: List[str], relevant: str, k: int) -> float:
    """Check if relevant content is in top-k retrieved chunks."""
    for chunk_text in retrieved[:k]:
        # Check if key terms from relevant appear in chunk
        relevant_terms = set(tokenize(relevant))
        chunk_terms = set(tokenize(chunk_text))
        overlap = len(relevant_terms & chunk_terms)
        if overlap >= min(3, len(relevant_terms)):
            return 1.0
    return 0.0


def mean_reciprocal_rank(retrieved: List[str], relevant: str) -> float:
    for i, chunk_text in enumerate(retrieved):
        relevant_terms = set(tokenize(relevant))
        chunk_terms = set(tokenize(chunk_text))
        overlap = len(relevant_terms & chunk_terms)
        if overlap >= min(3, len(relevant_terms)):
            return 1.0 / (i + 1)
    return 0.0


def bleu_score(reference: str, candidate: str, n: int = 2) -> float:
    """Simple BLEU-like score using n-gram precision."""
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)

    if len(cand_tokens) == 0:
        return 0.0

    # Count n-gram matches
    def get_ngrams(tokens, n):
        return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}

    precisions = []
    for n_val in range(1, n + 1):
        if len(cand_tokens) < n_val or len(ref_tokens) < n_val:
            precisions.append(0.0)
            continue
        ref_ngrams = get_ngrams(ref_tokens, n_val)
        cand_ngrams = get_ngrams(cand_tokens, n_val)
        if len(cand_ngrams) == 0:
            precisions.append(0.0)
            continue
        matches = len(ref_ngrams & cand_ngrams)
        precisions.append(matches / len(cand_ngrams))

    if not precisions or min(precisions) == 0:
        return 0.0
    return np.exp(np.mean(np.log(precisions)))


def rouge_l(reference: str, candidate: str) -> float:
    """ROUGE-L: F-measure based on longest common subsequence."""
    ref_tokens = tokenize(reference)
    cand_tokens = tokenize(candidate)

    # LCS length
    m, n = len(ref_tokens), len(cand_tokens)
    dp = np.zeros((m + 1, n + 1), dtype=np.int64)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_tokens[i - 1] == cand_tokens[j - 1]:
                dp[i, j] = dp[i - 1, j - 1] + 1
            else:
                dp[i, j] = max(dp[i - 1, j], dp[i, j - 1])
    lcs = dp[m, n]

    if lcs == 0:
        return 0.0
    precision = lcs / max(len(cand_tokens), 1)
    recall = lcs / max(len(ref_tokens), 1)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return f1


# ─────────────────────────────────────────────
# Main RAG Pipeline
# ─────────────────────────────────────────────

class RAGPipeline:
    def __init__(self, docs: List[str], chunk_size: int = 64, overlap: int = 16):
        print("Ingesting documents...")
        self.chunks = load_and_chunk_all(docs, chunk_size, overlap)
        self.vocab = build_vocab(self.chunks)
        self.idf = compute_idf(self.chunks, self.vocab)
        self.embeddings = embed_chunks(self.chunks, self.vocab, self.idf)
        self.store = VectorStore()
        self.store.add(self.chunks, self.embeddings)
        self.generator = SimpleGenerator()
        print(f"  {len(self.chunks)} chunks from {len(docs)} docs")
        print(f"  Vocab size: {len(self.vocab)}")

    def retrieve(self, query: str, k: int = 5) -> List[Tuple[Dict, float]]:
        query_vec = compute_tfidf(query, self.vocab, self.idf)
        norm = np.linalg.norm(query_vec)
        if norm > 0:
            query_vec = query_vec / norm
        return self.store.search(query_vec, k)

    def answer(self, query: str, k: int = 3) -> str:
        results = self.retrieve(query, k)
        if not results:
            return "No relevant information found."

        context = ' '.join([r['text'] for r, _ in results])
        answer = self.generator.generate(query, context)
        return answer

    def evaluate_retrieval(self, qa_pairs: List[Tuple[str, str]], k_values: List[int] = [1, 3, 5]) -> Dict:
        results = {}
        for k in k_values:
            recall_scores = []
            mrr_scores = []
            for query, relevant in qa_pairs:
                retrieved = self.retrieve(query, max(k, 5))
                retrieved_texts = [r['text'] for r, _ in retrieved]
                recall_scores.append(recall_at_k(retrieved_texts, relevant, k))
                mrr_scores.append(mean_reciprocal_rank(retrieved_texts, relevant))
            results[f'Recall@{k}'] = np.mean(recall_scores)
            results[f'MRR@{k}'] = np.mean(mrr_scores)
        return results

    def evaluate_generation(self, qa_pairs: List[Tuple[str, str]]) -> Dict:
        bleu_scores = []
        rouge_scores = []
        for query, relevant in qa_pairs:
            answer = self.answer(query)
            bleu_scores.append(bleu_score(relevant, answer))
            rouge_scores.append(rouge_l(relevant, answer))
        return {'BLEU': np.mean(bleu_scores), 'ROUGE-L': np.mean(rouge_scores)}


# ─────────────────────────────────────────────
# Ablation study
# ─────────────────────────────────────────────

def run_ablation():
    """Study effect of chunk size and top-K on retrieval quality."""
    chunk_sizes = [32, 64, 128]
    k_values = [1, 3, 5]

    results = {}
    for cs in chunk_sizes:
        pipe = RAGPipeline(DOCUMENTS, chunk_size=cs, overlap=cs // 4)
        for k in k_values:
            recall = pipe.evaluate_retrieval(QA_PAIRS, k_values=[k])
            key = f"cs={cs},k={k}"
            results[key] = recall[f'Recall@{k}']

    return results


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    np.random.seed(42)

    print("=" * 60)
    print("RAG SYSTEM WITH EVALUATION")
    print("=" * 60)

    # Build pipeline
    pipeline = RAGPipeline(DOCUMENTS, chunk_size=64, overlap=16)

    # ── Query Examples ──
    print("\n--- Query Examples ---")
    queries = [
        "What is machine learning?",
        "How do transformers work?",
        "Tell me about neural networks",
        "What is gradient descent?",
    ]
    for q in queries:
        ans = pipeline.answer(q)
        print(f"\nQ: {q}")
        print(f"A: {ans}")
        # Show retrieved chunks
        results = pipeline.retrieve(q, k=2)
        print(f"  (Retrieved: {[r['text'][:60] + '...' for r, _ in results]})")

    # ── Retrieval Evaluation ──
    print("\n--- Retrieval Evaluation ---")
    ret_metrics = pipeline.evaluate_retrieval(QA_PAIRS, k_values=[1, 3, 5])
    for metric, value in ret_metrics.items():
        print(f"  {metric}: {value:.4f}")

    # ── Generation Evaluation ──
    print("\n--- Generation Evaluation ---")
    gen_metrics = pipeline.evaluate_generation(QA_PAIRS[:10])
    for metric, value in gen_metrics.items():
        print(f"  {metric}: {value:.4f}")

    # ── Ablation ──
    print("\n--- Ablation Study ---")
    ablation_results = run_ablation()

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Retrieval metrics bar chart
    metrics_names = list(ret_metrics.keys())
    metrics_values = list(ret_metrics.values())
    colors = plt.cm.Blues(np.linspace(0.3, 0.8, len(metrics_names)))
    axes[0].bar(metrics_names, metrics_values, color=colors)
    axes[0].set_ylabel('Score')
    axes[0].set_title('Retrieval Performance')
    axes[0].set_ylim(0, 1)
    for i, v in enumerate(metrics_values):
        axes[0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontsize=9)
    axes[0].grid(alpha=0.3, axis='y')

    # Ablation heatmap
    cs_vals = [32, 64, 128]
    k_vals = [1, 3, 5]
    heatmap = np.zeros((len(cs_vals), len(k_vals)))
    for i, cs in enumerate(cs_vals):
        pipe = RAGPipeline(DOCUMENTS, chunk_size=cs, overlap=cs // 4)
        for j, k in enumerate(k_vals):
            recall = pipe.evaluate_retrieval(QA_PAIRS, k_values=[k])
            heatmap[i, j] = recall[f'Recall@{k}']

    im = axes[1].imshow(heatmap, cmap='Blues', aspect='auto')
    axes[1].set_xticks(range(len(k_vals)))
    axes[1].set_xticklabels([f'k={k}' for k in k_vals])
    axes[1].set_yticks(range(len(cs_vals)))
    axes[1].set_yticklabels([f'cs={cs}' for cs in cs_vals])
    axes[1].set_title('Recall@K by Chunk Size')
    for i in range(len(cs_vals)):
        for j in range(len(k_vals)):
            axes[1].text(j, i, f'{heatmap[i, j]:.3f}', ha='center', va='center', fontsize=9)
    plt.colorbar(im, ax=axes[1])

    plt.tight_layout()
    plt.savefig('../../assets/phase12/06_rag_results.png', dpi=150)
    plt.close()
    print("Saved 06_rag_results.png")


if __name__ == '__main__':
    main()

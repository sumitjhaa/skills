"""
09.20 LLM Evaluation — Perplexity, BERTScore Concept, Pairwise Judge
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


def perplexity(log_probs):
    """Perplexity = exp(-1/N * sum(log P(token)))"""
    return np.exp(-np.mean(log_probs))


def bertscore_sim(ref_embedding, candidate_embedding):
    """BERTScore-style cosine similarity between embeddings."""
    ref = ref_embedding / np.linalg.norm(ref_embedding)
    cand = candidate_embedding / np.linalg.norm(candidate_embedding)
    recall = ref @ cand
    precision = cand @ ref
    f1 = 2 * precision * recall / (precision + recall + 1e-10)
    return {"precision": precision, "recall": recall, "f1": f1}


def pairwise_judge(candidate_a, candidate_b, rubric):
    """LLM-as-a-judge: compare two candidate outputs against rubric."""
    # Simulated judge scoring
    a_score = np.random.rand()
    b_score = np.random.rand()
    winner = "A" if a_score > b_score else "B"
    return {
        "winner": winner,
        "scores": {"A": a_score, "B": b_score},
        "justification": f"Candidate {winner} better matches rubric: {rubric}",
    }


def evaluate_qa(answers, references):
    """Simple exact match and F1 scoring."""
    exact_matches = sum(1 for a, r in zip(answers, references) if a.strip() == r.strip())
    em = exact_matches / len(answers)
    # Token-level F1
    f1_scores = []
    for a, r in zip(answers, references):
        a_tokens = set(a.lower().split())
        r_tokens = set(r.lower().split())
        if not a_tokens or not r_tokens:
            f1_scores.append(0.0)
            continue
        overlap = a_tokens & r_tokens
        precision = len(overlap) / len(a_tokens)
        recall = len(overlap) / len(r_tokens)
        if precision + recall == 0:
            f1_scores.append(0.0)
        else:
            f1_scores.append(2 * precision * recall / (precision + recall))
    return {"exact_match": em, "f1": np.mean(f1_scores)}


if __name__ == "__main__":
    # Perplexity
    log_probs = np.random.randn(100) * 0.5 - 1.0
    ppl = perplexity(log_probs)
    print(f"Perplexity: {ppl:.2f}")

    # BERTScore style
    ref_emb = np.random.randn(64)
    cand_emb = np.random.randn(64)
    bs = bertscore_sim(ref_emb, cand_emb)
    print(f"BERTScore F1: {bs['f1']:.4f}")

    # Pairwise judge
    rubric = "factual accuracy, completeness, conciseness"
    judge_result = pairwise_judge("Answer A text", "Answer B text", rubric)
    print(f"Pairwise judge: Winner = {judge_result['winner']}")

    # QA metrics
    answers = ["Paris", "42", "Neural networks"]
    references = ["Paris", "42", "Deep learning"]
    metrics = evaluate_qa(answers, references)
    print(f"QA: EM={metrics['exact_match']:.2f}, F1={metrics['f1']:.3f}")

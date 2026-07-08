"""08.26 Visual QA and captioning: attention, transformers."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

img_size = 28
n_regions = 7
d_model = 64

img_features = np.random.randn(n_regions, d_model)
question_embed = np.random.randn(10, d_model)

def attention(Q, K, V, mask=None):
    scores = Q @ K.T / np.sqrt(d_model)
    if mask is not None:
        scores += mask
    weights = np.exp(scores) / np.exp(scores).sum(axis=-1, keepdims=True)
    return weights @ V, weights

Q = question_embed[-1:].copy()
K = img_features
V = img_features
attended, attn_weights = attention(Q, K, V)

answer_logits = np.random.randn(5)
answer_probs = np.exp(answer_logits) / np.exp(answer_logits).sum()

attention_map = attn_weights[0].copy()

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

img_display = np.random.rand(img_size, img_size) * 0.3
r = 3
for i in range(n_regions):
    cx = np.random.randint(r, img_size - r)
    cy = np.random.randint(r, img_size - r)
    yy, xx = np.ogrid[:img_size, :img_size]
    mask = (xx - cx)**2 + (yy - cy)**2 <= r**2
    img_display[mask] = 0.5 + 0.5 * attention_map[i]

axes[0, 0].imshow(img_display, cmap="Reds")
for i in range(n_regions):
    pass
axes[0, 0].set_title("Question: 'What color is the cat?'\nAttention over image regions")
axes[0, 0].axis("off")

axes[0, 1].bar(range(n_regions), attention_map, alpha=0.7)
axes[0, 1].set_xlabel("Image region")
axes[0, 1].set_ylabel("Attention weight")
axes[0, 1].set_title("Cross-Attention Weights\n(question → image)")
axes[0, 1].grid(True, alpha=0.3)

answers = ["cat", "dog", "car", "tree", "person"]
axes[0, 2].bar(answers, answer_probs, color=["orange", "blue", "green", "red", "purple"],
              alpha=0.7)
axes[0, 2].set_xlabel("Answer")
axes[0, 2].set_ylabel("Probability")
axes[0, 2].set_title(f"Answer: '{answers[np.argmax(answer_probs)]}'\n"
                     f"(conf={answer_probs.max():.3f})")
axes[0, 2].grid(True, axis="y", alpha=0.3)

caption_words = ["A", "cat", "sitting", "on", "a", "mat"]
n_caption = len(caption_words)
capt_attn = np.random.rand(n_caption, n_regions)
capt_attn /= capt_attn.sum(axis=1, keepdims=True)
axes[1, 0].imshow(capt_attn, cmap="Blues", aspect="auto")
axes[1, 0].set_xticks(range(n_regions))
axes[1, 0].set_yticks(range(n_caption))
axes[1, 0].set_xticklabels([f"R{i}" for i in range(n_regions)])
axes[1, 0].set_yticklabels(caption_words)
axes[1, 0].set_xlabel("Image region")
axes[1, 0].set_ylabel("Caption word")
axes[1, 0].set_title("Caption→Image Attention")
plt.colorbar(axes[1, 0].images[0], ax=axes[1, 0])

seq_len = 20
self_attn = 1 / (1 + np.abs(np.arange(seq_len)[:, None] - np.arange(seq_len)[None, :]))
axes[1, 1].imshow(self_attn, cmap="Blues")
axes[1, 1].set_xlabel("Token position")
axes[1, 1].set_ylabel("Token position")
axes[1, 1].set_title("Self-Attention Pattern\n(causal masking)")
plt.colorbar(axes[1, 1].images[0], ax=axes[1, 1])

n_heads = [1, 2, 4, 8, 16]
attn_param_counts = [h * d_model * 3 * d_model + h * d_model for h in n_heads]
axes[1, 2].plot(n_heads, np.array(attn_param_counts) / 1e3, "o-", lw=2)
axes[1, 2].set_xlabel("Number of attention heads")
axes[1, 2].set_ylabel("Attention params (K)")
axes[1, 2].set_title("MHA Parameter Count\n(d_model=64)")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/26-vqa-captioning.png")
plt.close()

print("=" * 60)
print("VISUAL QA AND CAPTIONING")
print("=" * 60)
print(f"\nVQA: Visual Question Answering")
print(f"  Question embedding: {question_embed.shape}")
print(f"  Image regions: {n_regions} × {d_model}")
print(f"  Predicted answer: '{answers[np.argmax(answer_probs)]}'")

print(f"\nCaption: {' '.join(caption_words)}")
print(f"  Caption length: {n_caption} words")
print(f"  Max attention region: region {np.argmax(capt_attn.sum(axis=0))}")

print(f"\nKey architectures:")
print(f"  • VQA: bottom-up attention + top-down")
print(f"    → Faster R-CNN for regions")
print(f"    → LSTM/Transformer for question")
print(f"    → MCB/MFH for multimodal fusion")
print(f"  • Show, Attend and Tell: spatial attention")
print(f"  • LXMERT: cross-modal transformer")
print(f"  • ViLT: vision-language transformer (no CNN)")
print(f"  • BLIP/BLIP-2: bootstrapped captioning")
print(f"  • LLaVA: large language + vision assistant")

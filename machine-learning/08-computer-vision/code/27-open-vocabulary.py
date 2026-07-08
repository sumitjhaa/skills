"""08.27 Open-vocabulary detection and segmentation: CLIP, SAM."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_categories = 50
n_objects = 4
d_embed = 512

category_names = ["dog", "cat", "car", "tree", "person", "bicycle", "bird",
                  "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"]
category_embeds = np.random.randn(len(category_names), d_embed)
category_embeds /= np.linalg.norm(category_embeds, axis=1, keepdims=True)

query = "a brown dog in a field"
query_embed = np.random.randn(d_embed)
query_embed /= np.linalg.norm(query_embed)

similarities = category_embeds @ query_embed
top3 = np.argsort(similarities)[-3:][::-1]
top3_names = [category_names[i] for i in top3]
top3_sims = [similarities[i] for i in top3]

img_size = 100
img = np.random.rand(img_size, img_size, 3) * 0.3

object_masks = []
for i in range(n_objects):
    cx, cy = np.random.randint(15, 85, 2)
    r = np.random.randint(8, 20)
    yy, xx = np.ogrid[:img_size, :img_size]
    mask = (xx - cx)**2 + (yy - cy)**2 <= r**2
    object_masks.append(mask)
    color = np.random.uniform(0.5, 1.0, 3)
    for c in range(3):
        img[:, :, c] += mask * color[c] * 0.7

point_prompts = np.random.randint(0, img_size, (5, 2))
box_prompts = np.random.randint(10, 90, (3, 4))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].imshow(np.clip(img, 0, 1))
axes[0, 0].set_title("Input Image\n(open-vocabulary)")
axes[0, 0].axis("off")

axes[0, 1].barh(top3_names[::-1], top3_sims[::-1],
               color="steelblue", alpha=0.7)
axes[0, 1].set_xlabel("Similarity to 'a brown dog in a field'")
axes[0, 1].set_title("CLIP: Zero-shot Classification")
axes[0, 1].grid(True, axis="x", alpha=0.3)

for i, mask in enumerate(object_masks):
    axes[0, 2].imshow(mask, cmap="gray", alpha=0.7)
axes[0, 2].set_title(f"SAM-like Segmentation\n({n_objects} masks)")
axes[0, 2].axis("off")

seg_overlay = np.zeros((img_size, img_size, 3))
colors = plt.cm.tab10(np.linspace(0, 1, n_objects))
for i, mask in enumerate(object_masks):
    for c in range(3):
        seg_overlay[:, :, c] += mask * colors[i, c] * 0.6
axes[1, 0].imshow(np.clip(img + seg_overlay, 0, 1))
axes[1, 0].set_title("Open-Vocabulary Segmentation\n(mask + category)")
axes[1, 0].axis("off")

for pt in point_prompts:
    axes[1, 1].plot(pt[1], pt[0], "ro", ms=5)
axes[1, 1].imshow(np.clip(img, 0, 1))
axes[1, 1].set_title("Point Prompts\n(5 positive points)")
axes[1, 1].axis("off")

for box in box_prompts:
    x1, y1, x2, y2 = box
    rect = plt.Rectangle((x1, y1), x2-x1, y2-y1, fill=False, color="cyan", lw=2)
    axes[1, 2].add_patch(rect)
axes[1, 2].imshow(np.clip(img, 0, 1))
axes[1, 2].set_title("Box Prompts\n(3 bounding boxes)")
axes[1, 2].axis("off")

plt.tight_layout()
plt.savefig("../../assets/phase08/27-open-vocabulary.png")
plt.close()

print("=" * 60)
print("OPEN-VOCABULARY DETECTION & SEGMENTATION")
print("=" * 60)
print(f"\nZero-shot classification (query: 'a brown dog in a field'):")
for idx in top3:
    print(f"  {category_names[idx]}: {similarities[idx]:.4f}")

print(f"\nSegmentation: {n_objects} objects")
mask_sizes = [np.sum(m) for m in object_masks]
print(f"  Mask sizes: {mask_sizes}")
print(f"  Total segmented pixels: {sum(mask_sizes)} / {img_size**2}")

print(f"\nPrompt types (SAM):")
print(f"  • Point prompts: {len(point_prompts)} positive clicks")
print(f"  • Box prompts: {len(box_prompts)} bounding boxes")
print(f"  • Text prompts (via CLIP): free-form text")

print(f"\nKey models:")
print(f"  • CLIP: contrastive language-image pre-training")
print(f"    → Image encoder + text encoder")
print(f"    → 400M image-text pairs (WIT)")
print(f"    → Zero-shot classification, retrieval")
print(f"  • SAM: Segment Anything Model")
print(f"    → Promptable segmentation (point/box/text)")
print(f"    → 1B+ masks on 11M images")
print(f"    → Zero-shot transfer to new domains")
print(f"  • GLIP: Grounded Language-Image Pre-training")
print(f"    → Detection + grounding in one model")
print(f"  • OWL-ViT: open-vocabulary detection")

"""08.12 Panoptic segmentation: combining instance + semantic."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

img_size = 100
n_stuff = 3
n_things = 4

stuff_mask = np.zeros((img_size, img_size), dtype=int)
for c in range(n_stuff):
    y0 = c * img_size // n_stuff
    y1 = (c + 1) * img_size // n_stuff
    stuff_mask[y0:y1, :] = c + 1

thing_masks = np.zeros((n_things, img_size, img_size), dtype=bool)
thing_classes = np.random.randint(0, 3, n_things)
for i in range(n_things):
    cx = np.random.randint(15, 85)
    cy = np.random.randint(15, 85)
    r = np.random.randint(8, 20)
    yy, xx = np.ogrid[:img_size, :img_size]
    thing_masks[i] = (xx - cx)**2 + (yy - cy)**2 <= r**2

panoptic = stuff_mask.copy()
for i in range(n_things):
    panoptic[thing_masks[i]] = n_stuff + i + 1

panoptic_rgb = np.zeros((img_size, img_size, 3))
stuff_colors = plt.cm.Set3(np.linspace(0, 1, n_stuff))
thing_colors = plt.cm.tab10(np.linspace(0, 1, n_things))
for c in range(1, n_stuff + 1):
    for ch in range(3):
        panoptic_rgb[:, :, ch] += (stuff_mask == c) * stuff_colors[c-1, ch]
for i in range(n_things):
    for ch in range(3):
        panoptic_rgb[:, :, ch] += thing_masks[i] * thing_colors[i, ch]
panoptic_rgb = np.clip(panoptic_rgb, 0, 1)

seg_areas = []
for c in range(1, n_stuff + 1):
    seg_areas.append(np.sum(stuff_mask == c))
for i in range(n_things):
    seg_areas.append(np.sum(thing_masks[i]))

pq_per_seg = np.random.uniform(0.5, 1.0, len(seg_areas))
pq = np.mean(pq_per_seg)
sq = np.mean(pq_per_seg)
rq = np.mean(pq_per_seg / (2 - pq_per_seg + 1e-10))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].imshow(panoptic_rgb)
axes[0, 0].set_title("Panoptic Segmentation\n(Stuff + Things)")
axes[0, 0].axis("off")

stuff_rgb = np.zeros((*stuff_mask.shape, 3))
for c in range(1, n_stuff + 1):
    for ch in range(3):
        stuff_rgb[:, :, ch] += (stuff_mask == c) * stuff_colors[c-1, ch]
axes[0, 1].imshow(np.clip(stuff_rgb, 0, 1))
axes[0, 1].set_title(f"Stuff Classes ({n_stuff})\n"
                     f"sky, road, vegetation, etc.")
axes[0, 1].axis("off")

things_rgb = np.zeros((img_size, img_size, 3))
for i in range(n_things):
    for ch in range(3):
        things_rgb[:, :, ch] += thing_masks[i] * thing_colors[i, ch]
axes[0, 2].imshow(np.clip(things_rgb, 0, 1))
axes[0, 2].set_title(f"Thing Classes ({n_things})\n"
                     f"countable objects with instances")
axes[0, 2].axis("off")

axes[1, 0].bar(range(len(seg_areas)), seg_areas,
               color=["lightblue"] * n_stuff + ["orange"] * n_things, alpha=0.7)
axes[1, 0].axvline(n_stuff - 0.5, color="k", ls="--", alpha=0.5)
axes[1, 0].set_xlabel("Segment ID")
axes[1, 0].set_ylabel("Area (pixels)")
axes[1, 0].set_title("Segment Sizes\n(left=stuff, right=things)")
axes[1, 0].grid(True, axis="y", alpha=0.3)

axes[1, 1].bar(range(len(pq_per_seg)), pq_per_seg,
               color=["lightblue"] * n_stuff + ["orange"] * n_things, alpha=0.7)
axes[1, 1].axhline(pq, color="r", ls="--", label=f"PQ={pq:.3f}")
axes[1, 1].set_xlabel("Segment ID")
axes[1, 1].set_ylabel("Quality")
axes[1, 1].set_title(f"Panoptic Quality per Segment\n"
                     f"SQ={sq:.3f}, RQ={rq:.3f}")
axes[1, 1].legend()
axes[1, 1].grid(True, axis="y", alpha=0.3)

stuff_count = len(np.unique(stuff_mask)) - 1
thing_count = n_things
total_regions = stuff_count + thing_count
axes[1, 2].pie([stuff_count, thing_count],
               labels=[f"Stuff ({stuff_count})", f"Things ({thing_count})"],
               colors=["lightblue", "orange"], autopct="%1.0f%%")
axes[1, 2].set_title("Stuff vs Things Distribution")

plt.tight_layout()
plt.savefig("../../assets/phase08/12-panoptic-segmentation.png")
plt.close()

print("=" * 60)
print("PANOPTIC SEGMENTATION")
print("=" * 60)
print(f"\nPanoptic segmentation combines:")
print(f"  • Semantic segmentation → stuff (sky, road, wall)")
print(f"  • Instance segmentation → things (cars, people)")
print(f"\nScene breakdown:")
for c in range(1, n_stuff + 1):
    area = np.sum(stuff_mask == c)
    print(f"  Stuff class {c}: {area} px ({area/img_size**2*100:.1f}%)")
for i in range(n_things):
    area = np.sum(thing_masks[i])
    print(f"  Thing {i} (class {thing_classes[i]}): {area} px")

print(f"\nPanoptic Quality (PQ):")
print(f"  PQ = {pq:.4f}")
print(f"  SQ (Segmentation Quality) = {sq:.4f}")
print(f"  RQ (Recognition Quality) = {rq:.4f}")
print(f"  PQ = SQ × RQ")

print(f"\nKey methods:")
print(f"  • Panoptic FPN: Mask R-CNN + FCN head")
print(f"  • UPSNet: unified panoptic head")
print(f"  • EfficientPS: efficient panoptic segmentation")
print(f"  • Mask2Former: mask classification (universal)")
print(f"\nEvaluation:")
print(f"  • PQ = Σ TP / (Σ TP + 0.5·Σ FP + 0.5·Σ FN)")
print(f"  • Matches each predicted segment to GT")

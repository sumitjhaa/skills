"""04.22 Lie groups and their algebras."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm, logm

def so3_hat(w):
    return np.array([[0, -w[2], w[1]], [w[2], 0, -w[0]], [-w[1], w[0], 0]])

def so3_vee(W):
    return np.array([W[2, 1], W[0, 2], W[1, 0]])

def se3_hat(xi):
    w, v = xi[:3], xi[3:]
    W = so3_hat(w)
    return np.vstack([np.hstack([W, v.reshape(-1, 1)]), np.zeros(4)])

def exp_map_so3(w, theta=None):
    if theta is None:
        theta = np.linalg.norm(w)
    if theta < 1e-10:
        return np.eye(3)
    w_hat = so3_hat(w / theta)
    return (np.eye(3) + np.sin(theta) * w_hat +
            (1 - np.cos(theta)) * w_hat @ w_hat)

def log_map_so3(R):
    theta = np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))
    if theta < 1e-10:
        return np.zeros(3)
    return theta / (2 * np.sin(theta)) * np.array([
        R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])

np.random.seed(42)
w1 = np.array([0.5, 0.3, -0.2])
R1 = exp_map_so3(w1)

w2 = log_map_so3(R1)

axis_range = np.linspace(0, 2*np.pi, 100)
Rs = [exp_map_so3(np.array([t, 0.3*t, 0])) for t in np.linspace(0, np.pi, 20)]

n_pts = 50
np.random.seed(0)
points_3d = np.random.randn(3, n_pts)
R_rand = exp_map_so3(np.array([0.5, -0.3, 0.8]))
points_rotated = R_rand @ points_3d

fig = plt.figure(figsize=(14, 9))
gs = fig.add_gridspec(2, 3)
axes_sub = [fig.add_subplot(gs[0, 0], projection="3d"),
            fig.add_subplot(gs[0, 1]),
            fig.add_subplot(gs[0, 2], projection="3d"),
            fig.add_subplot(gs[1, 0], projection="3d"),
            fig.add_subplot(gs[1, 1]),
            fig.add_subplot(gs[1, 2])]

ax = axes_sub[0]
u = np.linspace(0, 2*np.pi, 30)
v = np.linspace(0, np.pi, 30)
xs = np.outer(np.cos(u), np.sin(v))
ys = np.outer(np.sin(u), np.sin(v))
zs = np.outer(np.ones(30), np.cos(v))
ax.plot_surface(xs, ys, zs, alpha=0.1, color="blue")
ax.scatter([0, 0, 0], [0, 0, 0], [0, 0, 0], color="k", s=50)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title("SO(3) Rotations of Unit Sphere")

thetas = np.linspace(0, 2*np.pi, 50)
ax.plot(np.sin(thetas), np.zeros(50), np.cos(thetas), "r-", lw=2)
ax.plot(np.zeros(50), np.sin(thetas), np.cos(thetas), "g-", lw=2)

angles = np.linspace(0, np.pi, 50)
dist_from_id = []
for a in angles:
    R = exp_map_so3(np.array([a, 0, 0]))
    dist_from_id.append(np.linalg.norm(log_map_so3(R)))
axes_sub[1].plot(angles, dist_from_id, "b-", lw=2)
axes_sub[1].plot(angles, angles, "r--", lw=2, label="‖ω‖")
axes_sub[1].set_xlabel("True angle θ")
axes_sub[1].set_ylabel("‖log(R)‖")
axes_sub[1].set_title("Geodesic Distance on SO(3)")
axes_sub[1].legend()
axes_sub[1].grid(True, alpha=0.3)

axes_sub[2].scatter(points_3d[0], points_3d[1], points_3d[2], c="blue", alpha=0.5,
                    label="Original")
axes_sub[2].scatter(points_rotated[0], points_rotated[1], points_rotated[2], c="red",
                    alpha=0.7, label="Rotated")
axes_sub[2].set_xlabel("x"); axes_sub[2].set_ylabel("y"); axes_sub[2].set_zlabel("z")
axes_sub[2].set_title(f"SO(3) Rotation\n{len(points_3d)} random 3D points")
axes_sub[2].legend()

w_algebras = np.random.randn(10, 3)
exp_Rs = np.array([exp_map_so3(w / np.linalg.norm(w) * 0.5) for w in w_algebras])
log_ws = np.array([log_map_so3(R) for R in exp_Rs])
axes_sub[3].scatter(w_algebras[:, 0], w_algebras[:, 1], w_algebras[:, 2], c="blue", s=30,
                    label="𝔰𝔬(3) (algebra)")
axes_sub[3].scatter(log_ws[:, 0], log_ws[:, 1], log_ws[:, 2], c="red", s=30,
                    label="log(exp(w))")
axes_sub[3].set_xlabel("ω₁"); axes_sub[3].set_ylabel("ω₂"); axes_sub[3].set_zlabel("ω₃")
axes_sub[3].set_title("𝔰𝔬(3) Lie Algebra\nexp/log consistency")
axes_sub[3].legend()

bch_angles = np.linspace(0.01, 0.5, 20)
bch_errors = []
for a in bch_angles:
    w_a = np.array([a, 0, 0])
    w_b = np.array([0, a, 0])
    R_ab = exp_map_so3(w_a) @ exp_map_so3(w_b)
    w_ab = log_map_so3(R_ab)
    bch_errors.append(np.linalg.norm(w_ab - (w_a + w_b + 0.5 * np.cross(w_a, w_b))))
axes_sub[4].plot(bch_angles, bch_errors, "o-", lw=2)
axes_sub[4].set_xlabel("‖ω‖")
axes_sub[4].set_ylabel("BCH error (O(θ³))")
axes_sub[4].set_title("Baker-Campbell-Hausdorff\nApproximation Error")
axes_sub[4].grid(True, alpha=0.3)

adjoint_test = np.array([0.5, -0.3, 0.2])
R_test = exp_map_so3(np.array([0.3, 0.1, -0.2]))
adj_w = R_test @ adjoint_test
adj_R = R_test @ so3_hat(adjoint_test) @ R_test.T
axes_sub[5].bar(["Ad(R)ω", "R·ω̂·Rᵀ"],
                [np.linalg.norm(adj_w), np.linalg.norm(so3_vee(adj_R))],
                color=["blue", "orange"])
axes_sub[5].set_ylabel("Norm")
axes_sub[5].set_title("Adjoint Action\nAd(R)ω = Rω")
axes_sub[5].grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/22-lie-groups.png")
plt.close()

print("=" * 60)
print("LIE GROUPS AND LIE ALGEBRAS")
print("=" * 60)
print(f"\nSO(3) rotation from ω={w1}:")
print(f"  R = {np.round(R1, 4)}")
w2_rounded = np.round(w2, 6)
print(f"  log(R) = {w2_rounded}")
print(f"  Error: ‖ω - log(exp(ω))‖ = {np.linalg.norm(w1 - w2):.10f}")

print(f"\nBCH formula: log(exp(A)exp(B)) = A + B + ½[A,B] + ...")
print(f"  [A,B] = cross product for SO(3)")
print(f"  Max BCH error at θ=0.5: {bch_errors[-1]:.6f}")

print(f"\nKey concepts:")
print(f"  • SO(3): 3×3 rotation matrices (det=+1, RᵀR=I)")
print(f"  • 𝔰𝔬(3): 3-vectors with hat map (skew-symmetric)")
print(f"  • exp: 𝔰𝔬(3) → SO(3) (Rodrigues formula)")
print(f"  • log: SO(3) → 𝔰𝔬(3)")
print(f"  • Adjoint: Ad(R)ω = R·ω")

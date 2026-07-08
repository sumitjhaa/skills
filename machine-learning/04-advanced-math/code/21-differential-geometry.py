"""04.21 Differential geometry: geodesics on a sphere."""
import numpy as np

def sphere_metric(theta, phi):
    """Riemannian metric on S^2."""
    g = np.array([[1, 0], [0, np.sin(theta)**2]])
    return g

def christoffel_symbols(theta, phi):
    """Non-zero Christoffel symbols for S^2."""
    Gamma = np.zeros((2, 2, 2))
    Gamma[1, 1, 0] = -np.sin(theta) * np.cos(theta)
    Gamma[0, 1, 1] = Gamma[1, 0, 1] = np.cos(theta) / np.sin(theta)
    return Gamma

def geodesic_equation(t, y):
    theta, phi, dtheta, dphi = y
    Gamma = christoffel_symbols(theta, phi)
    ddtheta = -Gamma[1, 1, 0] * dphi * dphi - 2 * Gamma[0, 1, 0] * dtheta * dphi
    ddphi = -2 * Gamma[0, 1, 1] * dtheta * dphi - Gamma[1, 1, 1] * dphi * dphi
    return [dtheta, dphi, ddtheta, ddphi]

def solve_geodesic(y0, T=5.0, n_steps=1000):
    dt = T / n_steps
    y = np.array(y0)
    traj = [y.copy()]
    for _ in range(n_steps):
        k1 = np.array(geodesic_equation(0, y))
        k2 = np.array(geodesic_equation(0, y + 0.5 * dt * k1))
        k3 = np.array(geodesic_equation(0, y + 0.5 * dt * k2))
        k4 = np.array(geodesic_equation(0, y + dt * k3))
        y = y + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
        traj.append(y.copy())
    return np.array(traj)

# Great circle: equatorial path
y0 = [np.pi/2, 0.0, 0.0, 1.0]  # theta=pi/2, phi=0, dtheta=0, dphi=1
traj = solve_geodesic(y0, T=2*np.pi, n_steps=2000)
print(f"Geodesic on sphere (great circle):")
print(f"  Start: ({traj[0,0]:.4f}, {traj[0,1]:.4f})")
print(f"  End:   ({traj[-1,0]:.4f}, {traj[-1,1]:.4f})")
print(f"  Final phi - initial phi: {traj[-1,1] - traj[0,1]:.4f} (expected ~2*pi)")

# Gaussian curvature of sphere = 1/R^2
K_sphere = 1.0
print(f"Gaussian curvature of S^2: {K_sphere}")

# Exponential map on S^2 (from north pole)
def exp_map_sphere(v, R=1.0):
    theta = np.linalg.norm(v) / R
    if theta < 1e-10:
        return np.array([0, 0, R])
    direction = v / np.linalg.norm(v)
    x = R * np.sin(theta) * direction[0]
    y = R * np.sin(theta) * direction[1]
    z = R * np.cos(theta)
    return np.array([x, y, z])

v = np.array([0.5, 0.8])
pt = exp_map_sphere(v)
print(f"Exponential map at north pole with v={v}: {np.round(pt, 4)}")

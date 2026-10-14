#!/usr/bin/env python3
"""Write the explicit k-point list (file_kw) used by tutorial 007.

The list holds
  1. the time-reversal-reduced half of the Gamma-centered n x n x 1 mesh
     (k and -k are the same point without spin-orbit coupling; weight 2/n^2,
     or 1/n^2 for the four self-conjugate points), and
  2. a Gamma - M - K - Gamma path of NPATH points with weight 1e-9, so that the
     total energy, the DOS and the band edges come from one SCF run.

Coordinates are reduced (components along the reciprocal primitive vectors).
Usage: make_kpoints.py N NPATH > kmos_k.dat      (example: 36 54)
Use --full to keep the whole mesh (no time-reversal reduction).
"""
import sys


def mesh_points(n, reduce=True):
    half = n // 2
    seen, pts = set(), []
    for j in range(-half, n - half):
        for i in range(-half, n - half):
            key = (i % n, j % n)
            if key in seen:
                continue
            partner = ((-i) % n, (-j) % n)
            seen.add(key)
            if not reduce:
                pts.append(((i / n, j / n), 1.0 / n ** 2))
                continue
            seen.add(partner)
            pts.append(((i / n, j / n), (1.0 if partner == key else 2.0) / n ** 2))
    assert abs(sum(w for _, w in pts) - 1.0) < 1e-12
    return pts


def path_points(npath):
    """Gamma -> M(1/2,0) -> K(1/3,1/3) -> Gamma with exactly npath points."""
    s = npath - 1
    a2 = max(2, int(round(s / 4.732)))
    a1 = max(2, int(round(s * 1.732 / 4.732)))
    a3 = s - a1 - a2
    assert a3 >= 2
    G, M, K = (0.0, 0.0), (0.5, 0.0), (1.0 / 3.0, 1.0 / 3.0)
    out = []
    for t in range(a1):
        f = t / a1
        out.append((G[0] + f * (M[0] - G[0]), G[1] + f * (M[1] - G[1])))
    for t in range(a2):
        f = t / a2
        out.append((M[0] + f * (K[0] - M[0]), M[1] + f * (K[1] - M[1])))
    for t in range(a3 + 1):
        f = t / a3
        out.append((K[0] + f * (G[0] - K[0]), K[1] + f * (G[1] - K[1])))
    assert len(out) == npath
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    full = "--full" in sys.argv
    n, npath = int(args[0]), int(args[1])
    rows = [(k[0], k[1], w) for k, w in mesh_points(n, not full)]
    rows += [(k[0], k[1], 1e-9) for k in path_points(npath)]
    print(len(rows))
    for i, (kx, ky, w) in enumerate(rows, 1):
        print("%5d %.15f %.15f %.15f %.12e" % (i, kx, ky, 0.0, w))


if __name__ == "__main__":
    main()

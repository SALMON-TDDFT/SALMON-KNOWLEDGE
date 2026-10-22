"""Re eps_z at 1 eV (tau 10 fs) along the r and k ladders of tutorial 012, as is and baseline subtracted.
Values from provenance/ladder-script-output.txt (baseline table).
Usage: plot_re_eps_ladders.py <figure dir>"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = [16, 20, 24, 28, 32]
r_as = [4.932, 5.533, 5.666, 5.698, 5.708]
r_sub = [5.890, 5.883, 5.884, 5.884, 5.884]
k = [6, 8, 10, 12, 16, 20, 24]
k_as = [5.533, 5.592, 5.565, 5.563, 5.569, 5.577, 5.575]
k_sub = [5.883, 5.857, 5.813, 5.806, 5.803, 5.810, 5.808]

fig, ax = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
for a, x, y0, y1, ref, lab, refname in (
        (ax[0], r, r_as, r_sub, r_sub[-1], "r (real-space grid), k 6^3", "r32"),
        (ax[1], k, k_as, k_sub, k_sub[-1], "k mesh n^3, r20", "k24")):
    a.axhspan(ref * 0.99, ref * 1.01, color="tab:green", alpha=0.15, label=f"within 1 % of {refname} (subtracted)")
    a.plot(x, y0, "o--", color="0.55", label="as is")
    a.plot(x, y1, "s-", color="tab:blue", label="baseline subtracted")
    for xi, yi in zip(x, y1):
        a.annotate(f"{100 * (yi / ref - 1):+.2f} %", (xi, yi), textcoords="offset points", xytext=(0, 8),
                   ha="center", fontsize=8, color="tab:blue")
    a.set_xticks(x)
    a.set_xlabel(lab)
    a.grid(alpha=0.3)
ax[0].set_ylabel("Re eps_z at 1 eV (tau = 10 fs)")
ax[0].set_title("r ladder: as-is drop is the baseline, not the grid")
ax[1].set_title("k ladder: within 1.3 % from k6, 0.1 % from k10")
ax[0].legend(loc="lower right", fontsize=8)
ax[0].set_ylim(4.8, 6.1)
fig.suptitle("012: refractive index below the gap (Re eps_z at 1 eV) along the ladders")
fig.tight_layout()
fig.savefig(sys.argv[1] + "/re-eps-1ev-ladders.png", dpi=100)

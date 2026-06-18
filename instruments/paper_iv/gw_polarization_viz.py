"""#129 GW-POL -- visualization of the two wave types (intuition companion).

Shows how a ring of free test masses (and an L-shaped interferometer's two
arms) responds to:
  * the TENSOR + mode (GR / what LIGO measures): a traceless SHEAR -- the
    x-arm lengthens exactly as the y-arm shortens, so the differential
    readout L_x - L_y is maximal;
  * the SSV scalar mode (isotropic / breathing): a pure DILATION -- both arms
    lengthen together, so the differential readout CANCELS.

Writes papers/SSV-IV/figures/gw_pol_intuition.png and (if Pillow is present)
gw_pol_intuition.gif.  Not part of the test suite -- a teaching figure.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "papers" / "SSV-IV" / "figures"

H = 0.45              # strain amplitude, exaggerated for visibility
NRING = 28
ALPHA = np.linspace(0, 2 * np.pi, NRING, endpoint=False)
RING = np.stack([np.cos(ALPHA), np.sin(ALPHA)])   # (2, N) unit ring


def deform(phase, kind):
    """Return deformed ring (2,N) at a given wave phase for 'tensor' or 'ssv'."""
    s = H * np.cos(phase)
    if kind == "tensor":          # plus mode: x +, y -  (traceless shear)
        sx, sy = 1 + 0.5 * s, 1 - 0.5 * s
    else:                          # ssv isotropic / breathing: x +, y +
        sx, sy = 1 + 0.5 * s, 1 + 0.5 * s
    return np.stack([sx * RING[0], sy * RING[1]]), sx, sy


def _draw_ring(ax, kind, phase, title, subtitle):
    ax.set_aspect("equal")
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-2.0, 2.0)
    ax.axis("off")
    # undeformed reference
    ax.plot(RING[0], RING[1], ":", color="0.7", lw=1)
    d, sx, sy = deform(phase, kind)
    ax.scatter(d[0], d[1], s=18, color="0.25", zorder=3)
    # the two interferometer arms (x red, y blue), length tracks sx, sy
    cx = "#c0392b"
    cy = "#2471a3" if kind == "tensor" else "#c0392b"
    ax.annotate("", xy=(sx * 1.3, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=cx, lw=3))
    ax.annotate("", xy=(0, sy * 1.3), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=cy, lw=3))
    lab_x = "x-arm  +" if sx > 1 else "x-arm  −"
    lab_y = "y-arm  −" if (kind == "tensor") else "y-arm  +"
    ax.text(sx * 1.3 + 0.08, -0.22, lab_x, color=cx, ha="center", fontsize=9, weight="bold")
    ax.text(0.5, sy * 1.3 + 0.12, lab_y, color=cy, ha="left", fontsize=9, weight="bold")
    ax.set_title(title, fontsize=11, weight="bold", pad=14)
    ax.text(0, -2.25, subtitle, ha="center", fontsize=9, color="0.3")


def static_figure():
    fig = plt.figure(figsize=(11, 7.5))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1], hspace=0.32, wspace=0.15)

    ax_t = fig.add_subplot(gs[0, 0])
    ax_s = fig.add_subplot(gs[0, 1])
    # show each at the phase of maximum effect (cos = +1)
    _draw_ring(ax_t, "tensor", 0.0,
               "TENSOR (GR / LIGO): shear",
               "x stretches WHILE y shrinks  →  differential L$_x$−L$_y$ is maximal")
    _draw_ring(ax_s, "ssv", 0.0,
               "SSV scalar: breathing (isotropic)",
               "x and y stretch TOGETHER  →  differential L$_x$−L$_y$ cancels")

    ax = fig.add_subplot(gs[1, :])
    ph = np.linspace(0, 2 * np.pi, 400)
    # arm strains
    lx_t = 0.5 * H * np.cos(ph)
    ly_t = -0.5 * H * np.cos(ph)
    lx_s = 0.5 * H * np.cos(ph)
    ly_s = 0.5 * H * np.cos(ph)
    ax.plot(ph, lx_t - ly_t, color="#1a5276", lw=3,
            label="TENSOR  differential L$_x$−L$_y$  (full signal — what LIGO reads)")
    ax.plot(ph, lx_s - ly_s, color="#c0392b", lw=3.5,
            label="SSV  differential L$_x$−L$_y$  ≈ 0  (cancels; real residual ∝ fL/c is ~340× smaller)")
    ax.axhline(0, color="0.6", lw=0.8)
    ax.text(np.pi, 0.06, "SSV common-mode L$_x$+L$_y$ is real and large —\nbut a differential detector is structurally blind to it",
            ha="center", va="bottom", fontsize=8.5, color="0.35", style="italic")
    ax.set_xlabel("wave phase  ωt", fontsize=10)
    ax.set_ylabel("arm-length change", fontsize=10)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_xticks([0, np.pi, 2 * np.pi])
    ax.set_xticklabels(["0", "π", "2π"])
    ax.legend(loc="upper right", fontsize=8.5, framealpha=0.95)
    ax.set_title("What the interferometer actually reads out", fontsize=11, weight="bold")

    fig.suptitle("Two ways a wave can stretch space — and why only one drives a differential detector",
                 fontsize=12.5, weight="bold")
    FIG.mkdir(parents=True, exist_ok=True)
    out = FIG / "gw_pol_intuition.png"
    fig.savefig(out, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return out


def animation_gif():
    try:
        from matplotlib.animation import FuncAnimation, PillowWriter
    except Exception:
        return None
    fig, (axt, axs) = plt.subplots(1, 2, figsize=(9.5, 5))
    for ax in (axt, axs):
        ax.set_aspect("equal"); ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7); ax.axis("off")
    axt.set_title("TENSOR (GR / LIGO)\nshear: arms oppose", fontsize=11, weight="bold")
    axs.set_title("SSV scalar\nbreathing: arms together", fontsize=11, weight="bold")

    ref_t, = axt.plot(RING[0], RING[1], ":", color="0.7", lw=1)
    ref_s, = axs.plot(RING[0], RING[1], ":", color="0.7", lw=1)
    sc_t = axt.scatter(RING[0], RING[1], s=18, color="0.25")
    sc_s = axs.scatter(RING[0], RING[1], s=18, color="0.25")
    arm_tx, = axt.plot([0, 1.45], [0, 0], color="#c0392b", lw=4)
    arm_ty, = axt.plot([0, 0], [0, 1.45], color="#2471a3", lw=4)
    arm_sx, = axs.plot([0, 1.45], [0, 0], color="#c0392b", lw=4)
    arm_sy, = axs.plot([0, 0], [0, 1.45], color="#c0392b", lw=4)

    def update(i):
        phase = 2 * np.pi * i / 40
        dt, sxt, syt = deform(phase, "tensor")
        ds, sxs, sys = deform(phase, "ssv")
        sc_t.set_offsets(dt.T)
        sc_s.set_offsets(ds.T)
        arm_tx.set_data([0, 1.45 * sxt], [0, 0])
        arm_ty.set_data([0, 0], [0, 1.45 * syt])
        arm_sx.set_data([0, 1.45 * sxs], [0, 0])
        arm_sy.set_data([0, 0], [0, 1.45 * sys])
        return sc_t, sc_s, arm_tx, arm_ty, arm_sx, arm_sy

    anim = FuncAnimation(fig, update, frames=40, interval=80, blit=True)
    out = FIG / "gw_pol_intuition.gif"
    anim.save(out, writer=PillowWriter(fps=12))
    plt.close(fig)
    return out


if __name__ == "__main__":
    p = static_figure()
    print("wrote", p)
    g = animation_gif()
    print("wrote", g if g else "(GIF skipped: Pillow unavailable)")

"""Week 01 Thu — plot synthetic IMU.

Run after generate_imu.py:
    python weeks/week-01-numpy-imu/src/03_visualize.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "synthetic_imu.csv"
OUT_PATH = ROOT / "outputs" / "imu_raw.png"


def load_imu(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load CSV with header t,ax,ay,az.

    Return t shape (N,) and accel shape (N, 3).
    Hint: np.loadtxt(..., delimiter=',', skiprows=1)
    """
    # TODO
    raise NotImplementedError


def accel_magnitude(accel: np.ndarray) -> np.ndarray:
    # TODO: same as Wednesday
    raise NotImplementedError


def plot_imu(t: np.ndarray, accel: np.ndarray, mag: np.ndarray, path: Path) -> None:
    """Two-row figure: 3-axis accel, then magnitude. Save to path. Do not plt.show()."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # TODO: axes[0] plot ax, ay, az vs t with a legend
    # TODO: axes[1] plot mag vs t, label it
    # TODO: axes[1].set_xlabel("t (s)")
    # TODO: axes[0].set_ylabel("accel (m/s^2)")
    # TODO: axes[1].set_ylabel("|a| (m/s^2)")
    # TODO: axes[0].set_title("Synthetic IMU")

    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"Missing {CSV_PATH}. Run generate_imu.py first.")
    t, accel = load_imu(CSV_PATH)
    assert t.ndim == 1 and accel.shape == (t.shape[0], 3)
    mag = accel_magnitude(accel)
    assert mag.shape == t.shape
    plot_imu(t, accel, mag, OUT_PATH)
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()

"""Generate a tiny synthetic IMU CSV for week 01.

This is not a physically perfect IMU. It is a teaching signal:
still → accel → coast → brake → still, plus gravity and noise.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

FS_HZ = 100.0
DURATION_S = 12.0
GRAVITY = 9.81
NOISE_STD = 0.04
SEED = 7

SEGMENTS = (
    # (t_start, t_end, body_ax_mps2)  — extra specific force on X, besides gravity
    (0.0, 2.0, 0.0),
    (2.0, 4.0, 1.5),
    (4.0, 6.0, 0.0),
    (6.0, 8.0, -1.5),
    (8.0, 12.0, 0.0),
)


def synthetic_accel(t: np.ndarray) -> np.ndarray:
    ax = np.zeros_like(t)
    for t0, t1, value in SEGMENTS:
        ax[(t >= t0) & (t < t1)] = value
    # last sample of last segment
    ax[t >= SEGMENTS[-1][0]] = SEGMENTS[-1][2]

    ay = np.zeros_like(t)
    az = np.full_like(t, GRAVITY)
    return np.column_stack([ax, ay, az])


def main() -> None:
    rng = np.random.default_rng(SEED)
    n = int(FS_HZ * DURATION_S)
    t = np.arange(n, dtype=np.float64) / FS_HZ
    accel = synthetic_accel(t) + rng.normal(0.0, NOISE_STD, size=(n, 3))

    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "synthetic_imu.csv"

    header = "t,ax,ay,az"
    data = np.column_stack([t, accel])
    np.savetxt(path, data, delimiter=",", header=header, comments="", fmt="%.6f")
    print(f"wrote {path}  samples={n}  fs={FS_HZ} Hz")


if __name__ == "__main__":
    main()

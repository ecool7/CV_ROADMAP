"""Неделя 1, пятница. Лаборатория IMU. В воскресенье добавишь сглаживание.

Запуск:
    python weeks/week-01-numpy-imu/src/imu_lab.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "synthetic_imu.csv"
OUT_DIR = ROOT / "outputs"

# Порог «едет / стоит». В пятницу можно подкрутить, если маска кривая.
MOVE_THRESHOLD = 0.3
STILL_WINDOW_S = 1.0
FS_HZ = 100.0
# Воскресенье: поставь 10 и нарисуй сырой и сглаженный модуль вместе.
SMOOTH_WINDOW = 1


def load_imu(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Прочитай CSV. Можно взять ту же реализацию, что в 03_visualize.py."""
    raise NotImplementedError


def magnitude(accel: np.ndarray) -> np.ndarray:
    """Модуль ускорения на каждый отсчёт."""
    raise NotImplementedError


def estimate_g(mag: np.ndarray, fs: float, still_s: float) -> float:
    """Оцени g как медиану модуля на первых still_s секундах (генератор стартует из покоя)."""
    raise NotImplementedError


def moving_mask(mag: np.ndarray, g: float, threshold: float) -> np.ndarray:
    """True там, где прибор едет: |модуль − g| больше порога. Тип bool."""
    raise NotImplementedError


def moving_average(x: np.ndarray, window: int) -> np.ndarray:
    """Скользящее среднее той же длины, что x. Задание на воскресенье.

    В пятницу можно оставить return x.copy(), чтобы скрипт уже бежал.
    """
    if window <= 1:
        return x.copy()
    return x.copy()


def plot_lab(
    t: np.ndarray,
    mag: np.ndarray,
    mag_smooth: np.ndarray,
    moving: np.ndarray,
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    axes[0].plot(t, mag, label="|a| сырой", linewidth=1)
    if not np.allclose(mag, mag_smooth):
        axes[0].plot(t, mag_smooth, label="|a| сглаженный", linewidth=1.5)
    axes[0].legend()
    axes[0].set_ylabel("|a| (м/с²)")
    axes[0].set_title("Лаборатория IMU: стоит / едет")

    axes[1].plot(t, moving.astype(float), drawstyle="steps-post")
    axes[1].set_ylabel("едет")
    axes[1].set_xlabel("t (с)")
    axes[1].set_ylim(-0.1, 1.1)

    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    t, accel = load_imu(CSV_PATH)
    mag = magnitude(accel)
    g = estimate_g(mag, FS_HZ, STILL_WINDOW_S)
    moving = moving_mask(mag, g, MOVE_THRESHOLD)
    mag_smooth = moving_average(mag, SMOOTH_WINDOW)

    moving_s = float(moving.mean() * (t[-1] - t[0]))
    print(f"g_est     = {g:.3f} м/с²")
    print(f"mag mean  = {mag.mean():.3f}")
    print(f"mag std   = {mag.std():.3f}")
    print(f"moving    = {moving_s:.2f} с  ({100.0 * moving.mean():.1f}% записи)")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_name = "imu_lab_smoothed.png" if SMOOTH_WINDOW > 1 else "imu_lab.png"
    plot_lab(t, mag, mag_smooth, moving, OUT_DIR / out_name)
    print(f"записал {OUT_DIR / out_name}")


if __name__ == "__main__":
    main()

"""Неделя 1, пятница утро. Нарисовать синтетический IMU.

Сначала один раз запусти generate_imu.py, потом этот файл:
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
    """Прочитай CSV с заголовком t,ax,ay,az.

    Верни время t (длина N) и таблицу accel (N×3).
    """
    raise NotImplementedError


def accel_magnitude(accel: np.ndarray) -> np.ndarray:
    """Модуль ускорения на каждый момент времени. Как magnitude вчера."""
    raise NotImplementedError


def plot_imu(t: np.ndarray, accel: np.ndarray, mag: np.ndarray, path: Path) -> None:
    """Два графика друг под другом: три оси accel и модуль. Сохрани в файл, окно не открывай."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # верхний график: три оси ax, ay, az против времени, с легендой
    # нижний график: модуль против времени
    # подписи осей: время в секундах, ускорение в м/с²

    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"Нет файла {CSV_PATH}. Сначала запусти generate_imu.py.")
    t, accel = load_imu(CSV_PATH)
    assert t.ndim == 1 and accel.shape == (t.shape[0], 3)
    mag = accel_magnitude(accel)
    assert mag.shape == t.shape
    plot_imu(t, accel, mag, OUT_PATH)
    print(f"записал {OUT_PATH}")


if __name__ == "__main__":
    main()

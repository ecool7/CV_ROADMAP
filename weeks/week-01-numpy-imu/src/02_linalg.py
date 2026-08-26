"""Неделя 1, четверг. Линейная алгебра в NumPy на данных IMU.

Запуск:
    python weeks/week-01-numpy-imu/src/02_linalg.py
"""

from __future__ import annotations

import numpy as np


def magnitude(accel: np.ndarray) -> np.ndarray:
    """Длина каждого вектора ускорения (норма строки).

    На вход таблица N×3, на выход один столбец длины N.
    """
    raise NotImplementedError


def demean_per_axis(accel: np.ndarray) -> np.ndarray:
    """Из каждого столбца вычти его среднее. Размер тот же N×3."""
    raise NotImplementedError


def rotate_vector(R: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Поверни один вектор: v' = R v. v длины 3, R размера 3×3."""
    raise NotImplementedError


def rotate_batch(R: np.ndarray, accel: np.ndarray) -> np.ndarray:
    """Поверни каждый отсчёт той же матрицей R. Таблица N×3 → N×3."""
    raise NotImplementedError


def rotation_about_z(deg: float) -> np.ndarray:
    """Матрица поворота вокруг оси +Z. Угол в градусах, размер 3×3.
    Правило правой руки.
    """
    raise NotImplementedError


def main() -> None:
    accel = np.array(
        [
            [0.0, 0.0, 9.81],
            [3.0, 4.0, 0.0],
            [0.0, 0.0, 0.0],
        ]
    )
    mag = magnitude(accel)
    assert mag.shape == (3,)
    assert np.allclose(mag[0], 9.81)
    assert np.allclose(mag[1], 5.0)

    centered = demean_per_axis(accel)
    assert centered.shape == (3, 3)
    assert np.allclose(centered.mean(axis=0), 0.0)

    R90 = rotation_about_z(90.0)
    assert R90.shape == (3, 3)
    x = np.array([1.0, 0.0, 0.0])
    x_rot = rotate_vector(R90, x)
    assert np.allclose(x_rot, [0.0, 1.0, 0.0], atol=1e-8)

    batch = rotate_batch(R90, accel)
    assert batch.shape == accel.shape
    assert np.allclose(batch[0, 2], 9.81)
    assert np.allclose(batch[1, :2], [-4.0, 3.0])
    print("02_linalg: ALL PASSED")


if __name__ == "__main__":
    main()

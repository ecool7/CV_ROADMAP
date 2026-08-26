"""Неделя 1. IMU — таблица: строка = момент времени, столбцы = оси x y z.

По строкам циклом for не ходи. Запускай этот файл, пока не появится ALL PASSED.
"""

from __future__ import annotations

import numpy as np


def make_accel() -> np.ndarray:
    """Собери учебную запись акселерометра.

    Пять моментов времени, три оси:
    покой, рывок по x=1, рывок по x=2, снова покой, снова покой.
    В покое x=0, y=0, z=9.81 (тяжесть).
    """
    return np.array([[0, 0, 9.81],[1, 0, 9.81],[2, 0, 9.81],[0, 0, 9.81],[0, 0, 9.81]])


def n_samples(accel: np.ndarray) -> int:
    """Сколько моментов времени в таблице? Верни целое число — число строк."""
    return len(accel)


def z_axis(accel: np.ndarray) -> np.ndarray:
    """Верни только столбец z (вертикаль) на все моменты времени."""
    return accel[:,2]


def first_two_samples(accel: np.ndarray) -> np.ndarray:
    """Верни первые два момента времени целиком: и x, и y, и z."""
    return accel[0:2,:]


def samples_where_ax_positive(accel: np.ndarray) -> np.ndarray:
    """Верни только те моменты, где по оси x значение больше нуля (два рывка)."""
    return accel[accel[:,0] > 0]

def swap_xy(accel: np.ndarray) -> np.ndarray:
    """Верни копию таблицы: столбцы x и y поменялись местами, z не трогай.

    Исходную таблицу не меняй.
    """
    accel1= accel.copy()
    accel1[:,0] = accel[:,1]
    accel1[:,1] = accel[:,0]

    return accel1


def main() -> None:
    accel = make_accel()
    assert accel.shape == (5, 3), f"ожидали таблицу 5×3, получили {accel.shape}"
    assert n_samples(accel) == 5
    z = z_axis(accel)
    assert z.shape == (5,)
    assert np.allclose(z, 9.81)
    head = first_two_samples(accel)
    assert head.shape == (2, 3)
    assert np.allclose(head[0], [0.0, 0.0, 9.81])
    moved = samples_where_ax_positive(accel)
    assert moved.shape == (2, 3)
    assert np.all(moved[:, 0] > 0)
    swapped = swap_xy(accel)
    assert np.allclose(swapped[:, 0], accel[:, 1])
    assert np.allclose(swapped[:, 1], accel[:, 0])
    assert np.allclose(accel[0], [0.0, 0.0, 9.81]), "исходную таблицу менять нельзя"
    print("01_arrays: ALL PASSED")


if __name__ == "__main__":
    main()

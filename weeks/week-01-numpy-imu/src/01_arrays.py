"""Week 01 Tue — NumPy arrays on IMU-shaped data.

Rule: no `for` over samples. If you want a loop, there is a NumPy op for it.

Run:
    python weeks/week-01-numpy-imu/src/01_arrays.py
"""

from __future__ import annotations

import numpy as np

def make_accel() -> np.ndarray:
    """Return a fake accel array with shape (5, 3). Do not type numbers by hand
    as five separate lists if you can help it — use np.array once.
    """
    # TODO: array of 5 samples, axes x/y/z:
    #   [0, 0, 9.81]
    #   [1, 0, 9.81]
    #   [2, 0, 9.81]
    #   [0, 0, 9.81]
    #   [0, 0, 9.81]
    raise NotImplementedError


def n_samples(accel: np.ndarray) -> int:
    """How many time samples? Use .shape, not len() on a guess."""
    # TODO
    raise NotImplementedError


def z_axis(accel: np.ndarray) -> np.ndarray:
    """Return the z column, shape (N,)."""
    # TODO
    raise NotImplementedError


def first_two_samples(accel: np.ndarray) -> np.ndarray:
    """Return samples 0 and 1, shape (2, 3)."""
    # TODO
    raise NotImplementedError


def samples_where_ax_positive(accel: np.ndarray) -> np.ndarray:
    """Boolean mask indexing: rows where x-axis > 0. Shape (K, 3)."""
    # TODO
    raise NotImplementedError


def swap_xy(accel: np.ndarray) -> np.ndarray:
    """Return a copy where x and y columns are swapped. Do not modify input."""
    # TODO
    raise NotImplementedError


def main() -> None:
    accel = make_accel()
    assert accel.shape == (5, 3), f"expected (5, 3), got {accel.shape}"
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
    assert np.allclose(accel[0], [0.0, 0.0, 9.81]), "do not modify the input array"
    print("01_arrays: ALL PASSED")


if __name__ == "__main__":
    main()

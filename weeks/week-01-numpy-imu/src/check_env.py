"""Проверка, что Python, NumPy и matplotlib установлены."""

from __future__ import annotations

import sys


def main() -> None:
    print(f"python: {sys.version.split()[0]}")
    try:
        import numpy as np
        import matplotlib

        print(f"numpy: {np.__version__}")
        print(f"matplotlib: {matplotlib.__version__}")
    except ImportError as exc:
        print(f"MISSING PACKAGE: {exc}")
        print("Activate .venv and run: pip install -r requirements.txt")
        sys.exit(1)

    print("env: OK")


if __name__ == "__main__":
    main()

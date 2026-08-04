#!/usr/bin/env python3
"""Compatibilidad: redirige sync legacy al validador/reconciliación por ID."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_consistency import main as validate_main  # noqa: E402


def main() -> int:
    print("data:sync-csv ahora valida consistencia por ficha_id (sin sync por título).")
    return validate_main([])


if __name__ == "__main__":
    raise SystemExit(main())

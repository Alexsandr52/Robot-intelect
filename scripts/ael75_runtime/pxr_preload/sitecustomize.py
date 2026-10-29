"""Prefer Isaac Sim's bundled USD modules over other installed ``pxr`` providers."""

from pathlib import Path
import sys


USD_EXTENSION_ROOTS = list(Path("/isaac-sim/extscache").glob("omni.usd.libs-*"))
if len(USD_EXTENSION_ROOTS) == 1:
    sys.path.insert(0, str(USD_EXTENSION_ROOTS[0]))

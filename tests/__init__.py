"""Test suite for Student Record Manager."""

import sys
from pathlib import Path

# Add src and project root to sys.path so tests can run in any environment
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
ROOT_DIR = Path(__file__).resolve().parent.parent

if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

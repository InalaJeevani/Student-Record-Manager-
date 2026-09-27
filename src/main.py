"""Entry point when executing from the src directory.

Allows running `python src/main.py` or importing from src directly.
"""

import os
import sys
from pathlib import Path

# Add src and project root to sys.path to enable flexible importing
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import and execute main from root main.py or run CLI directly
if __name__ == "__main__":
    from main import main
    main()

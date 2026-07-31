"""Make the script directories importable (their names contain spaces)."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(ROOT, "2d Brillouin Zone"))
sys.path.insert(0, os.path.join(ROOT, "3d Brillouin Zone"))

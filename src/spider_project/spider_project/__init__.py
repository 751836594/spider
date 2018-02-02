import os

import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(parent_dir)
sys.path.insert(0, parent_dir)

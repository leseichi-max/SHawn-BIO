# 01-Analysis/verify_brain.py
import os
import sys

curr_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(curr_dir)
sys.path.append(os.path.join(root_dir, "99-System"))

try:
    from shawn_brain_v4 import SHawnBrainV4
    print("✅ Successfully imported SHawnBrainV4 from 99-System")
    brain = SHawnBrainV4(use_ensemble=False)
    print("✅ Successfully initialized SHawnBrainV4")
except Exception as e:
    print(f"❌ Failed to initialize brain: {e}")

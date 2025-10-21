#!/usr/bin/env python3
"""
ERP System Demo - Entry Point
This is the main entry point for the ERP system demo.
"""

import subprocess
import sys

if __name__ == "__main__":
    # Simply run the main run.py script
    subprocess.call(["python3", "run.py"] + sys.argv[1:])
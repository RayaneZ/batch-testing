#!/usr/bin/env python3
"""
Simple test runner for shtest_compiler.
This script provides easy access to the test suite from the src directory.
"""

import os
import sys
from pathlib import Path

# Add the testing directory to the path
testing_dir = Path(__file__).parent / "testing"
sys.path.insert(0, str(testing_dir))

# Import and run the test suite
from test_suite import main

if __name__ == "__main__":
    main()

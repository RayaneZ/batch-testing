#!/usr/bin/env python3
"""
Debug script to analyze what the parser produces for failing files.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from shtest_compiler.parser.configurable_parser import ConfigurableParser


def debug_file(file_path: str):
    """Debug a single file to see what the parser produces."""
    print(f"\n{'='*60}")
    print(f"DEBUGGING: {file_path}")
    print(f"{'='*60}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"File content ({len(content)} chars):")
        print("-" * 40)
        print(repr(content))
        print("-" * 40)

        # Test the modular parser first
        print("\n1. Testing ConfigurableParser:")
        try:
            parser = ConfigurableParser(debug=True)
            tokens = list(parser.lexer.lex(content))
            print(f"   Tokens ({len(tokens)}):")
            for i, token in enumerate(tokens[:10]):  # Show first 10 tokens
                print(f"     {i}: {token.kind} = '{token.value}' (line {token.lineno})")
            if len(tokens) > 10:
                print(f"     ... and {len(tokens) - 10} more tokens")

            # Try to parse
            ast = parser.parse(content, path=file_path)
            print(f"   AST built successfully:")
            print(f"     Steps: {len(ast.steps)}")
            for i, step in enumerate(ast.steps):
                print(
                    f"       Step {i}: '{step.name}' with {len(step.actions)} actions"
                )
                for j, action in enumerate(step.actions):
                    print(
                        f"         Action {j}: cmd='{action.command}', result='{action.result_expr}'"
                    )
                    print(f"           Raw line: '{action.raw_line}'")

        except Exception as e:
            print(f"   ConfigurableParser failed: {e}")

        # Legacy parser test removed - using only ConfigurableParser

    except Exception as e:
        print(f"Error reading file: {e}")


def main():
    """Debug all files in the ko directory."""
    ko_dir = Path(__file__).parent

    # Debug a few specific files first
    test_files = [
        "completely_empty.shtest",
        "empty_file.shtest",
        "invalid_syntax_1.shtest",
        "invalid_syntax_2.shtest",
        "invalid_syntax_3.shtest",
    ]

    for test_file in test_files:
        file_path = ko_dir / test_file
        if file_path.exists():
            debug_file(str(file_path))
        else:
            print(f"File not found: {file_path}")


if __name__ == "__main__":
    main()

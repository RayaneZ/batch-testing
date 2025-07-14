#!/usr/bin/env python3

from shtest_compiler.compiler.matchers.basic_checks_matcher import (
    load_patterns, strip_accents)


def debug_matcher():
    patterns = load_patterns()
    test_input = "fichier present"
    normalized = strip_accents(test_input.lower())

    print(f"Test input: '{test_input}'")
    print(f"Normalized: '{normalized}'")
    print(f"Total patterns loaded: {len(patterns)}")

    # Check file_present pattern specifically
    fp_pattern = patterns.get("Le fichier est présent")
    if fp_pattern:
        print(f"\nFile present pattern found:")
        print(f"  Handler: {fp_pattern['handler']}")
        print(f"  Scope: {fp_pattern['scope']}")

        aliases = fp_pattern["aliases"]
        print(f"  Raw aliases ({len(aliases)}):")
        for alias in aliases:
            print(f"    '{alias}'")

        # Check normalized aliases
        normalized_aliases = [
            strip_accents(alias.lower())
            for alias in aliases
            if not alias.startswith("^")
        ]
        print(f"\n  Normalized aliases ({len(normalized_aliases)}):")
        for alias in normalized_aliases:
            print(f"    '{alias}'")

        # Check if our input matches
        if normalized in normalized_aliases:
            print(f"\n✓ MATCH FOUND! '{normalized}' is in normalized aliases")
        else:
            print(f"\n✗ NO MATCH! '{normalized}' is NOT in normalized aliases")
            print(f"  Available normalized aliases: {normalized_aliases}")
    else:
        print("File present pattern NOT found!")


if __name__ == "__main__":
    debug_matcher()

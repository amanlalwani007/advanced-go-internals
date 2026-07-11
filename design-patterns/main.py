#!/usr/bin/env python3
"""
Design Patterns in Python — All 23 Gang of Four Patterns
Practical real-world examples for each pattern.
"""

import importlib
import pkgutil
import sys


def run_module(mod_name: str) -> None:
    print(f"\n{'='*70}")
    print(f"  {mod_name}")
    print(f"{'='*70}")
    try:
        mod = importlib.import_module(mod_name)
        if hasattr(mod, "main"):
            mod.main()
    except Exception as e:
        print(f"  ERROR: {e}")


def main() -> None:
    patterns = [
        # Creational
        "creational.prototype",
        # Structural
        "structural.bridge",
        "structural.composite",
        "structural.facade",
        "structural.flyweight",
        # Behavioral
        "behavioral.interpreter",
        "behavioral.iterator",
        "behavioral.mediator",
        "behavioral.memento",
        "behavioral.template_method",
        "behavioral.visitor",
        # Interview-Important (moved from categories)
        "interview_important.singleton",
        "interview_important.factory_method",
        "interview_important.abstract_factory",
        "interview_important.builder",
        "interview_important.adapter",
        "interview_important.decorator",
        "interview_important.proxy",
        "interview_important.observer",
        "interview_important.strategy",
        "interview_important.command",
        "interview_important.chain_of_responsibility",
        "interview_important.state",
    ]

    print("=" * 70)
    print("  23 GANG OF FOUR DESIGN PATTERNS — Python Implementation")
    print("  * Interview-important patterns marked with *")
    print("=" * 70)

    for pat in patterns:
        run_module(pat)

    print(f"\n{'='*70}")
    print("  All 23 patterns completed.")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()

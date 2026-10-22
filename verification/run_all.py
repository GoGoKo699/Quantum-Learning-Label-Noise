"""Run every finite verification suite; optionally save its actual JSON output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import sys

import numpy as np

import verify_repository
import verify_source_bell
import verify_statistics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Save the complete report to this path")
    args = parser.parse_args()
    report = {
        "schema_version": 1,
        "environment": {"python": platform.python_version(), "numpy": np.__version__},
        "scope": "Finite numerical and documentation checks; analytic proofs are in science/.",
        "suites": {},
    }
    success = True
    for name, module in (
        ("source_bell_reduction", verify_source_bell),
        ("statistics", verify_statistics),
        ("repository", verify_repository),
    ):
        try:
            result = module.run_checks()
            passed = result.get("passed", result.get("status") == "passed")
        except Exception as error:
            result = {"passed": False, "error_type": type(error).__name__, "error": str(error)}
            passed = False
        report["suites"][name] = result
        success = success and bool(passed)
    report["passed"] = success
    serialized = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Preflight checks for the OMML Formula Skill.

Checks required system/program dependencies and Python packages before an agent
attempts Office file mutation. Emits clear output for humans or JSON for agents.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from typing import Any

REQUIRED_PYTHON = ["lxml", "docx", "pptx"]
OPTIONAL_PYTHON = ["matplotlib"]
REQUIRED_PROGRAMS = ["pandoc"]


def program_version(executable: str) -> str | None:
    path = shutil.which(executable)
    if not path:
        return None
    try:
        proc = subprocess.run([executable, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
        first_line = proc.stdout.splitlines()[0] if proc.stdout else path
        return first_line
    except Exception:  # noqa: BLE001
        return path


def package_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def scan() -> dict[str, Any]:
    programs = {name: {"ok": shutil.which(name) is not None, "version": program_version(name)} for name in REQUIRED_PROGRAMS}
    required_python = {name: package_available(name) for name in REQUIRED_PYTHON}
    optional_python = {name: package_available(name) for name in OPTIONAL_PYTHON}
    ok = all(item["ok"] for item in programs.values()) and all(required_python.values())
    return {
        "ok": ok,
        "python": sys.version.split()[0],
        "programs": programs,
        "required_python_packages": required_python,
        "optional_python_packages": optional_python,
        "install_hint": "Install Pandoc and run: pip install -r requirements.txt. For PNG fallback: pip install -r requirements-optional.txt",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check OMML Formula Skill dependencies.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    args = parser.parse_args()
    result = scan()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Python: {result['python']}")
        for name, item in result["programs"].items():
            print(f"{name}: {'OK' if item['ok'] else 'MISSING'}" + (f" ({item['version']})" if item.get("version") else ""))
        for name, ok in result["required_python_packages"].items():
            print(f"python package {name}: {'OK' if ok else 'MISSING'}")
        for name, ok in result["optional_python_packages"].items():
            print(f"optional package {name}: {'OK' if ok else 'MISSING'}")
        if not result["ok"]:
            print(result["install_hint"])
    if not result["ok"]:
        sys.exit(2)


if __name__ == "__main__":
    main()

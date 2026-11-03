#!/usr/bin/env python3
"""Keep manifest.json's "systems" list equal to the files in systems/.

The app downloads exactly the ids listed there (falling back to the GitHub
API only when the list is missing). An id without its file aborts the whole
update; a file missing from the list is never downloaded. Run after adding,
removing or renaming a system file. --check exits 1 when the list is stale.
"""
import json
import sys
from pathlib import Path


def main():
    root = Path(__file__).parent
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    systems = sorted(p.stem for p in (root / "systems").glob("*.json"))

    if manifest.get("systems") == systems:
        print(f"OK: manifest lists all {len(systems)} systems.")
        return

    if "--check" in sys.argv:
        print("FAIL: manifest.json systems list is out of date.")
        sys.exit(1)

    manifest["systems"] = systems
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Updated: manifest lists {len(systems)} systems.")


if __name__ == "__main__":
    main()

"""Validate Quality Compass answer keys and report category coverage.

Usage: python validate_keys.py
Exits with status 1 if any answer key has errors.
"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
MIN_REQUIRED_PER_CATEGORY = 2


def load_codes():
    """Read valid risk codes from the taxonomy table so there is one source of truth."""
    text = (ROOT / "taxonomy.md").read_text()
    return set(re.findall(r"^\| ([A-Z0-9]+) \|", text, flags=re.MULTILINE)) - {"Code"}


def check_risk(risk, where, codes, errors):
    for field in ("id", "primary", "alternates", "description"):
        if field not in risk:
            errors.append(f"{where}: missing '{field}'")
    if risk.get("primary") not in codes:
        errors.append(f"{where}: unknown primary code {risk.get('primary')!r}")
    for alt in risk.get("alternates") or []:
        if alt not in codes:
            errors.append(f"{where}: unknown alternate code {alt!r}")
        if alt == risk.get("primary"):
            errors.append(f"{where}: alternate repeats primary code {alt!r}")


def validate(path, codes, seen_ids, required_counts):
    errors = []
    key = yaml.safe_load(path.read_text())
    name = path.name

    for field in ("id", "title", "request", "scoring", "planted_ambiguities",
                  "required_risks", "bonus_risks", "traps"):
        if field not in key:
            errors.append(f"{name}: missing '{field}'")
    if errors:
        return errors

    if key["id"] != path.stem:
        errors.append(f"{name}: id {key['id']!r} does not match file name")
    if key["id"] in seen_ids:
        errors.append(f"{name}: duplicate request id {key['id']!r}")
    seen_ids.add(key["id"])

    ambiguities = key["planted_ambiguities"] or []
    scoring = key["scoring"]
    if bool(ambiguities) != bool(scoring.get("ambiguity_recall")):
        errors.append(f"{name}: ambiguity_recall must be true exactly when ambiguities exist")
    if scoring.get("over_questioning_check") and "max_new_questions" not in scoring:
        errors.append(f"{name}: over_questioning_check needs max_new_questions")
    if not key["required_risks"]:
        errors.append(f"{name}: needs at least one required risk")

    item_ids = [a["id"] for a in ambiguities]
    for section in ("required_risks", "bonus_risks"):
        for i, risk in enumerate(key[section] or []):
            check_risk(risk, f"{name} {section}[{i}]", codes, errors)
            item_ids.append(risk.get("id"))
    item_ids += [t["id"] for t in key["traps"] or []]
    dupes = [i for i, n in Counter(item_ids).items() if n > 1]
    if dupes:
        errors.append(f"{name}: duplicate item ids {dupes}")

    for risk in key["required_risks"]:
        required_counts[risk.get("primary")] += 1
    return errors


def main():
    codes = load_codes()
    seen_ids, required_counts, errors = set(), Counter(), []
    files = sorted((ROOT / "answer_keys").glob("*.yaml"))
    for path in files:
        errors += validate(path, codes, seen_ids, required_counts)

    print(f"Checked {len(files)} answer keys against {len(codes)} risk codes.\n")
    print("Required-risk coverage by primary code:")
    for code in sorted(codes):
        n = required_counts[code]
        flag = "" if n >= MIN_REQUIRED_PER_CATEGORY else f"  <- below {MIN_REQUIRED_PER_CATEGORY}"
        print(f"  {code:5} {n}{flag}")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("\nNo schema errors.")


if __name__ == "__main__":
    main()

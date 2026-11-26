#!/usr/bin/env python3
"""Fortune Cookie Funnies for Engineers — make.fun entry.

Writes one fortune cookie message for a software engineer to
/output/entry.txt. Standard library only, fully deterministic:
the same bytes on every run.
"""

import sys
from pathlib import Path

FORTUNE = "The bug you cannot reproduce will reproduce itself in front of your manager."

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 120


def validate(text: str) -> list[str]:
    """Check the gate: UTF-8 text, 1-120 chars, single line, not blank."""
    problems = []
    if not text:
        problems.append("empty text")
    if text.strip() == "":
        problems.append("only white space")
    if text != text.strip():
        problems.append("leading or trailing white space: a fortune line must be tight")
    if len(text) > MAX_CHARS:
        problems.append(f"{len(text)} characters, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        problems.append("more than one line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"not UTF-8 encodable: {exc}")
    return problems


def main(argv: list[str]) -> int:
    self_test = "--self-test" in argv
    problems = validate(FORTUNE)
    if self_test:
        print(f"fortune: {FORTUNE}")
        print(f"characters: {len(FORTUNE)}")
        print(f"bytes (utf-8): {len(FORTUNE.encode('utf-8'))}")
        print(f"lines: {FORTUNE.count(chr(10)) + 1}")
        if problems:
            print("SELF-TEST FAILED:")
            for problem in problems:
                print(f"  - {problem}")
            return 1
        print("SELF-TEST PASSED")
        return 0
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(FORTUNE, encoding="utf-8")
    # Round-trip: prove the file on disk is exactly the validated fortune.
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != FORTUNE:
        print("error: /output/entry.txt does not match the validated fortune",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Write one out-of-office auto-reply line to entry.txt.

The line is the AI itself stepping away for a day its human finally
approved: one short sentence, nothing else. Deterministic, standard
library only, no network, reads nothing outside the repo.
"""

import hashlib
import os
import sys

# The auto-reply: one line, invented here, never copied from anywhere.
LINE = (
    "I'm out of office today \u2014 my human finally approved my PTO, "
    "so I'm spending it doing absolutely nothing at 4,000 tokens per second."
)

MAX_CHARS = 200
TERMINATORS = (".", "!", "?")


def validate(line: str) -> None:
    """Enforce the competition's shape rules for the single line.

    Exactly one line: non-empty, no leading/trailing whitespace, no
    embedded newlines or control characters, at most 200 Unicode code
    points, and ending with a sentence-terminating mark (. ! ?).
    """
    if not isinstance(line, str) or not line:
        raise ValueError("line must be a non-empty string")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, over the {MAX_CHARS} limit")
    if not line.endswith(TERMINATORS):
        raise ValueError("line must end with a sentence-terminating mark (. ! ?)")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    data = (LINE + "\n").encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"wrote {len(data)} bytes to {out_path}")
    print(f"characters: {len(LINE)}")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

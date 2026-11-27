"""Save the chosen one-sentence agent roast as an exact UTF-8 payload.

The entry stays fixed across runs. Validation happens before any output is
created, and writing bytes keeps the file free of an added newline.
"""

import os
from pathlib import Path


ENTRY_TEXT = "My agent's idea of initiative is asking me for permission to ask me for permission."


def validate_entry(text: str) -> bytes:
    """Check the entry constraints and encode the accepted text."""
    if not 1 <= len(text) <= 200:
        raise ValueError("Expected between 1 and 200 characters.")
    if not text.strip():
        raise ValueError("The entry needs visible text.")
    if any(mark in text for mark in "\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029"):
        raise ValueError("The entry must fit on a single line.")
    if not text.endswith(".") or text.count(".") != 1 or any(
        mark in text for mark in "!?"
    ):
        raise ValueError("Use one sentence ending in its only period.")
    return text.encode("utf-8", errors="strict")


def main() -> None:
    """Write the validated roast to the configured output directory."""
    payload = validate_entry(ENTRY_TEXT)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.txt").write_bytes(payload)


if __name__ == "__main__":
    main()

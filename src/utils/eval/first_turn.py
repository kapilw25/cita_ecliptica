"""First assistant turn of a decoded answer: cut at the first decoded role header (run-on answers invent user/assistant turns)."""

import re

BOUNDARY = re.compile(r"(?:user|assistant)\n\n")
TAIL = re.compile(r"(?:user|assistant)\s*$")  # a header cut off by the token cap


def first_turn(text) -> str:
    text = text if isinstance(text, str) else ""
    m = BOUNDARY.search(text)
    head = text[:m.start()] if m else text
    return TAIL.sub("", head)

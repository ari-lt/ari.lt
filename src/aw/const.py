#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Constants"""

from typing import Dict, Final, FrozenSet

HUGEINT_MAX: Final[int] = (10**65) - 1

USERNAME_SIZE: Final[int] = 64

NAME_SIZE: Final[int] = 256
WEBSITE_SIZE: Final[int] = 256
EMAIL_CT_SIZE: Final[int] = 256
COMMENT_SIZE: Final[int] = 1024

ALLOWED_TAGS: Final[FrozenSet[str]] = frozenset(
    (
        "em",
        "strong",
        "a",
        "code",
        "pre",
        "blockquote",
        "p",
        "ul",
        "ol",
        "li",
        "br",
    )
)

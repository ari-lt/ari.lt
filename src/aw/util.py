#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""utilities"""

import bleach
from markdown import markdown
from markupsafe import Markup

from . import const


def markdown_to_html(text: str) -> Markup:
    """Convert Markdown text to safe HTML"""

    return Markup(
        bleach.clean(
            markdown(text, extensions=("extra", "smarty")),
            tags=const.ALLOWED_TAGS,
            attributes={
                "*": ["href", "title"],
                "a": ["href"],
            },
            protocols={"http", "https"},
        )
    )

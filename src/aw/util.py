#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""utilities"""

from html import escape as html_escape

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


def text2svg(
    text: str,
    fill: str = "#fff",
    font: str = "sans-serif",
    size: float = 16,
    baseline: float = 1,
    padding: float = 1,
    ratio: float = 1,  # usually 2 for monospace
) -> str:
    """convert count to svg

    fill -- text colour
    font -- font family
    size -- font size in pixels
    baseline -- baseline offset
    padding -- padding of characters
    ratio -- character ratio

    embedding :

    <img
        id="my-stuff"
        src="..."
        style="display:inline;height:1em;vertical-align:top"
        alt="my stuff :3"
    />
    """

    fill = html_escape(fill)
    font = html_escape(font)

    svg: str = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{len(text) + padding * ratio}ch" height="{size}" font-size="{size}">'
    )
    svg += f'<text x="50%" y="{size - baseline}" text-anchor="middle" fill="{fill}" font-family="{font}">{html_escape(text)}</text>'
    svg += "</svg>"

    return svg

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ari.lt"""

from warnings import filterwarnings as filter_warnings

from flask import Flask

from aw import create_app

app: Flask = create_app(__name__)


def main() -> int:
    """entry/main function"""

    app.run("127.0.0.1", 8080, True)

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"

    filter_warnings("error", category=Warning)
    raise SystemExit(main())

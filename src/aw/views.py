#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""views"""

import typing as t

import flask
from werkzeug.wrappers import Response

from .routing import Bp
from .c import c

views: Bp = Bp("views", __name__)


@views.get("/index.html", alias=True)
@views.get("/")
def index() -> str:
    """Home page"""
    return flask.render_template("index.j2")


@views.get("/manifest.json")
def manifest() -> t.Any:
    """Manifest file"""
    return flask.jsonify(  # type: ignore
        {
            "$schema": "https://json.schemastore.org/web-manifest-combined.json",
            "short_name": "Ari::web -> Index",
            "name": "Ari::web -> Index",
            "description": "Personal website of Ari Archer. Providing free and open source services for everyone.",
            "icons": [{"src": "/favicon.ico", "sizes": "128x128", "type": "image/png"}],
            "start_url": ".",
            "display": "standalone",
            "theme_color": "#fbfbfb",
            "background_color": "#000000",
        }
    )


@views.get("/page/<path:p>")
def page(p: str) -> str:
    """Page renderer"""
    return p


@views.get("/LICENSE", alias=True)
@views.get("/license")
def license() -> flask.Response:
    """License: AGPL-3.0-or-later"""

    try:
        with open("../LICENSE", "r") as fp:
            return flask.Response(fp.read(), mimetype="text/plain")
    except Exception:
        with open("LICENSE", "r") as fp:
            return flask.Response(fp.read(), mimetype="text/plain")

@views.post("/")
def comment() -> flask.Response:
    """publish a comment"""
    return flask.Response(
        c.new().rawpng(),
        mimetype="image/png"
    )


@views.get("/git", defaults={"_": ""})
@views.get("/git/", defaults={"_": ""})
@views.get("/git/<path:_>")
def git(_: str) -> Response:
    """Git source code"""
    return flask.redirect(
        f"https://ari.lt/lh/us.ari.lt/{flask.request.full_path[4:]}",
        code=302,
    )


@views.get("/favicon.ico")
def favicon() -> Response:
    """Website icon"""
    return flask.redirect(
        flask.url_for(
            "static",
            filename="favicons/ari-web-lgbt.ico",
            mimetype="image/vnd.microsoft.icon",
        )
    )

@views.get("/captcha.png")
def captcha() -> flask.Response:
    """CAPTCHA"""
    return flask.Response(
        c.new().rawpng(),
        mimetype="image/png"
    )


@views.get("/badge.png")
def badge() -> Response:
    """Website badge"""
    return flask.redirect(
        flask.url_for(
            "static",
            filename="badges/badge.png",
        )
    )


@views.get("/badge-yellow.png")
def badge_yellow() -> Response:
    """Website badge (yellow)"""
    return flask.redirect(
        flask.url_for(
            "static",
            filename="badges/badge-yellow.png",
        )
    )

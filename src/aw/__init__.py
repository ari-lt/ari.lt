#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ari.lt"""

import datetime
import os
import sys
from base64 import b64encode
from functools import lru_cache
from typing import Any

import flask
import web_mini
from werkzeug.middleware.proxy_fix import ProxyFix

from . import util


@lru_cache
def min_css(css: str) -> str:
    """minify css"""
    return web_mini.css.minify_css(css)


@lru_cache(maxsize=64)
def min_html(html: str) -> str:
    """minify html"""
    return web_mini.html.minify_html(html)


def create_app(name: str) -> flask.Flask:
    """create ari.lt app"""

    for var in ("DB", "EMAIL_USER", "EMAIL_SERVER", "EMAIL_PASSWORD"):
        if var not in os.environ:
            print(f"Environment variable {var} is unset.", file=sys.stderr)
            sys.exit(1)

    app: flask.Flask = flask.Flask(name)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)  # type: ignore

    app.config["PREFERRED_URL_SCHEME"] = "http" if app.debug else "https"
    app.config["DOMAIN"] = "ari.lt"

    app.config["SECRET_KEY"] = os.urandom(4096)

    app.config["SESSION_COOKIE_SAMESITE"] = "strict"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB"]
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["CAPTCHA_PEPPER_FILE"] = "captcha.key"
    app.config["CAPTCHA_EXPIRY"] = 60 * 10  # 10 minutes
    app.config["CAPTCHA_CHARSET"] = "abdefghmnqrtyABDEFGHLMNRTY2345689#@%?!"
    app.config["CAPTCHA_RANGE"] = (4, 6)

    app.config["USE_SESSION_FOR_NEXT"] = True

    from .models import Counter, db

    with app.app_context():
        db.init_app(app)
        db.create_all()

        if db.session.query(Counter).count() < 1:
            print("Creating a website counter...")
            db.session.add(Counter(int(input("Count: "))))

        db.session.commit()

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .c import c

    c.init_app(app)

    app.jinja_env.filters["markdown"] = util.markdown_to_html  # type: ignore

    web_mini.compileall()

    @app.after_request
    def _(response: flask.Response) -> flask.Response:
        """minify resources and add headers"""

        if not app.debug:
            response.headers["Content-Security-Policy"] = "upgrade-insecure-requests"
            response.headers["Strict-Transport-Security"] = (
                "max-age=63072000; includeSubDomains; preload"
            )

        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        if response.direct_passthrough:
            return response

        if response.content_type == "text/html; charset=utf-8":
            minified_data: str = min_html(response.get_data(as_text=True))
        elif response.content_type == "text/css; charset=utf-8":
            minified_data: str = min_css(response.get_data(as_text=True))
        else:
            return response

        return app.response_class(  # type: ignore
            response=minified_data,
            status=response.status,
            headers=dict(response.headers),
            mimetype=response.mimetype,
        )

    @app.context_processor  # type: ignore
    def _() -> Any:
        """Context processor"""

        y: int = datetime.datetime.now(datetime.timezone.utc).year  # type: ignore

        return {
            "current_year": y,
            "ari_age": int((datetime.datetime.now() - datetime.datetime(2007, 9, 10)).days // 365.25),  # type: ignore
            "programming_exp": y - 2016,
            "python_exp": y - 2016,
            "c_exp": y - 2020,
            "b64encode": b64encode,
        }

    return app

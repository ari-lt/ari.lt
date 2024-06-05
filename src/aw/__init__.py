#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ari.lt"""

import datetime
import hashlib
import os
import sys
from typing import Any

import flask


def create_app(name: str) -> flask.Flask:
    """create ari.lt app"""

    for var in ("DB",):
        if var not in os.environ:
            print(f"Environment variable {var} is unset.", file=sys.stderr)
            sys.exit(1)

    app: flask.Flask = flask.Flask(name)

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

    from .models import Admin, db

    with app.app_context():
        db.init_app(app)
        db.create_all()

        # if db.session.query(Admin).count() < 1:
        #     print("Creating an admin account...")

        #     full_name: str = input("Full name: ")
        #     email: str = input("Email: ")
        #     salt: bytes = os.urandom(64)
        #     pwhash: bytes = hashlib.sha3_512(salt + input("Password: ")).digest()

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .c import c

    c.init_app(app)

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
        }

    return app

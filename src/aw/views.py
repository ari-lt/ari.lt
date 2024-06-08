#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""views"""

import datetime
import os
import typing as t

import flask
import validators
from werkzeug.wrappers import Response

from . import email, models, util
from .routing import Bp

views: Bp = Bp("views", __name__)
status: t.Dict[str, t.Any] = {
    "status": "<i>No status</i>",
    "last_updated": datetime.datetime.now(datetime.timezone.utc),
}


@views.get("/status")
def get_status() -> t.Any:
    """Get status"""
    return flask.jsonify(  # type: ignore
        {
            "status": status["status"],
            "last_updated": status["last_updated"].timestamp(),
        }
    )


@views.post("/status")
def set_status() -> Response:
    """Set status"""

    if (
        "status" in flask.request.form
        and flask.request.headers.get("X-Admin-Key", None) == os.environ["ADMIN_KEY"]
    ):
        status["status"] = str(flask.request.form["status"])  # type: ignore
        status["last_updated"] = datetime.datetime.now(datetime.timezone.utc)
        return flask.jsonify(  # type: ignore
            {
                "status": status["status"],
                "last_updated": status["last_updated"].timestamp(),
            }
        )
    else:
        flask.abort(401)


@views.get("/index.html", alias=True)
@views.get("/")
def index() -> str:
    """Home page"""

    return flask.render_template(
        "index.j2",
        visitor=models.Counter.first().inc().count,
        comments=models.Comment.query.filter_by(confirmed=True).order_by(
            models.Comment.posted.desc()  # type: ignore
        ),
        status=status,
    )


@views.get("/confirm/<int:comment_id>/<string:token>/", alias=True)
@views.get("/confirm/<int:comment_id>/<string:token>")
def confirm(comment_id: int, token: str):
    """confirm publishing of a comment"""

    comment: models.Comment = models.Comment.query.filter_by(
        id=comment_id, token=token, confirmed=False
    ).first_or_404()

    comment.confirmed = True

    models.db.session.commit()

    email.sendmail(
        "ari@ari.lt",
        f"Comment #{comment.id} on the guestbook",
        f"""New comment on the guestbook for you to check out.


URL: {flask.url_for("views.index")}#{comment.id}
Name: {comment.name}
Website: {comment.website}
Comment:

```
{comment.comment}
```

Deletion token:

    {comment.token}""",
    )

    flask.flash(f"Comment #{comment.id} confirmed.")

    return flask.redirect(flask.url_for("views.index"))


@views.get("/delete/<int:comment_id>/<string:token>/", alias=True)
@views.get("/delete/<int:comment_id>/<string:token>")
def delete(comment_id: int, token: str):
    """delete a comment"""

    comment: models.Comment = models.Comment.query.filter_by(
        id=comment_id, token=token
    ).first_or_404()

    models.db.session.delete(comment)
    models.db.session.commit()

    flask.flash(f"Comment #{comment.id} deleted.")

    return flask.redirect(flask.url_for("views.index"))


@views.post("/")
def comment():
    """publish a comment"""

    for field in "name", "email", "comment":
        if field not in flask.request.form:
            flask.abort(400)

    if not validators.email(flask.request.form["email"]):
        flask.abort(400)

    if (
        "website" in flask.request.form
        and flask.request.form["website"]
        and not validators.url(flask.request.form["website"])
    ):
        flask.abort(400)

    try:
        comment: models.Comment = models.Comment(
            flask.request.form["name"],  # type: ignore
            flask.request.form.get("website", None),  # type: ignore
            flask.request.form["email"],  # type: ignore
            flask.request.form["comment"],  # type: ignore
        )
    except Exception:
        flask.abort(400)

    models.db.session.add(comment)
    models.db.session.commit()

    try:
        email.sendmail(
            flask.request.form["email"],  # type: ignore
            f"Email confirmation for guestbook comment #{comment.id}",
            f"""Hello!

You (or someone) have commented on the {flask.request.url} guestbook. If it was you, please confirm your email address below. Otherwise - you may ignore this email or delete the comment by visiting the "delete" URL below.

The comment content includes your email (which will be listed publicly), as well as:

Name: {comment.name}
Website: {comment.website or "<none>"}
Comment:

```
{comment.comment}
```

Visit the following URL to *confirm* the comment:

    {flask.request.url.rstrip("/")}{flask.url_for("views.confirm", comment_id=comment.id, token=comment.token)}

Or you may *delete* the comment (even if you haven't confirmed it yet) by going to:

    {flask.request.url.rstrip("/")}{flask.url_for("views.delete", comment_id=comment.id, token=comment.token)}

You may delete the comment at any point.

If clicking the link does not work, try pasting it into your browser or running `curl`/`wget`/`axel`/... on it :)

Please do not reply to this email and if you have any questions - email Ari Archer <ari@ari.lt> with the GPG key 4FAD63E936B305906A6C4894A50D5B4B599AF8A2.""",
        )
    except Exception:
        models.db.session.delete(comment)
        models.db.session.commit()
        flask.abort(400)

    flask.flash("Check your mailbox.")

    return flask.redirect(flask.url_for("views.index"))


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


@views.get("/git", defaults={"_": ""})
@views.get("/git/", defaults={"_": ""})
@views.get("/git/<path:_>")
def git(_: str) -> Response:
    """Git source code"""
    return flask.redirect(
        f"/lh/ari.lt/{flask.request.full_path[4:]}",
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


@views.get("/counter.svg")
def counter() -> flask.Response:
    """counter"""
    return flask.Response(
        util.text2svg(
            text=str(models.Counter.first().inc().count),
            fill=flask.request.args.get("fill", "#fff"),
            font=flask.request.args.get("font", "sans-serif"),
            size=float(flask.request.args.get("size", 16)),
            baseline=float(flask.request.args.get("baseline", 1)),
            padding=float(flask.request.args.get("padding", 1)),
            ratio=float(flask.request.args.get("radio", 1)),
        ),
        mimetype="image/svg+xml",
    )


@views.get("/badge.png")
def badge() -> Response:
    """Website badge"""
    r: Response = flask.redirect(
        flask.url_for(
            "static",
            filename="badges/badge.png",
        )
    )

    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, HEAD"

    return r


@views.get("/badge-yellow.png")
def badge_yellow() -> Response:
    """Website badge"""
    r: Response = flask.redirect(
        flask.url_for(
            "static",
            filename="badges/badge-yellow.png",
        )
    )

    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, HEAD"

    return r


@views.get("/btc")
def btc() -> Response:
    """Bitcoin address"""
    return flask.redirect(
        "https://www.blockchain.com/explorer/addresses/btc/bc1qn3k75kmyvpw9sc58t63hk4ej4pc0d0w52tvj7w"
    )


@views.get("/xmr")
def xmr() -> Response:
    """Monero address"""
    return flask.redirect(
        "https://moneroexplorer.org/search?value=451VZy8FPDXCVvKWkq5cby3V24ApLnjaTdwDgKG11uqbUJYjxQWZVKiiefi4HvFd7haeUtGFRBaxgKNTr3vR78pkMzgJaAZ"
    )


@views.get("/page/canary", alias=True)
@views.get("/canary")
def canary():
    """Warrant Canary"""
    return "Unavailable due to migration reasons."


@views.get("/page/casey", alias=True)
@views.get("/casey")
def casey():
    """Open letter to my best friend"""
    return "Unavailable due to migration reasons."


@views.get("/page/matrix", alias=True)
@views.get("/matrix")
def matrix():
    """Matrix homeserver guidelines and Registration"""
    return "Unavailable due to migration reasons."


@views.get("/mp")
def mp():
    """Music playlist"""
    return flask.redirect(
        "https://www.youtube.com/playlist?list=PL7UuKajElTaChff3BkcJE6620lSuSUaDC"
    )


@views.get("/dotfiles", defaults={"_": ""})
@views.get("/dotfiles/", defaults={"_": ""})
@views.get("/dotfiles/<path:_>")
def dotfiles(_: str) -> Response:
    """Dotfiles"""
    return flask.redirect(
        f"https://github.com/TruncatedDinoSour/dotfiles-cleaned/{flask.request.full_path[9:]}",
        code=302,
    )


@views.get("/gh", defaults={"_": ""})
@views.get("/gh/", defaults={"_": ""})
@views.get("/gh/<path:_>")
def gh(_: str) -> Response:
    """Main git account"""
    return flask.redirect(
        f"https://github.com/TruncatedDinoSour/{flask.request.full_path[3:]}",
        code=302,
    )


@views.get("/lh", defaults={"_": ""})
@views.get("/lh/", defaults={"_": ""})
@views.get("/lh/<path:_>")
def lh(_: str) -> Response:
    """Main git organization account"""
    return flask.redirect(
        f"https://github.com/ari-lt/{flask.request.full_path[3:]}",
        code=302,
    )

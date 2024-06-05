#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DB Models"""

import datetime
import string
import typing as t
from decimal import Decimal
from secrets import SystemRandom

import crc4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DECIMAL, DateTime, Dialect, TypeDecorator, Unicode

from . import const

db: SQLAlchemy = SQLAlchemy()
rand: SystemRandom = SystemRandom()


class HugeUInt(TypeDecorator):  # type: ignore
    """huge int type, 0 to (10**64)-1"""

    impl: t.Any = DECIMAL

    def load_dialect_impl(self, dialect: Dialect) -> t.Any:
        """load dialect impl"""
        return dialect.type_descriptor(DECIMAL(65, 0))  # type: ignore

    def process_bind_param(
        self,
        value: t.Optional[t.Any],
        dialect: Dialect,
    ) -> t.Optional[int]:
        """process binding"""

        assert dialect is dialect

        if value is not None:
            if value < 0 or value > const.HUGEINT_MAX:
                raise ValueError("HugeUInt out of range [0;HUGEINT_MAX]")
            else:
                return int(value)
        else:
            return None

    def process_result_value(
        self,
        value: t.Optional[t.Any],
        dialect: Dialect,
    ) -> t.Optional[Decimal]:
        """process dialect"""
        assert dialect is dialect
        return Decimal(value) if value is not None else None


class Counter(db.Model):
    """Counter"""

    id: int = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
    )
    count: int = db.Column(HugeUInt())

    def __init__(self, count: int = 0) -> None:
        assert count >= 0 and count <= const.HUGEINT_MAX, "count out of range"
        self.count: int = count


class Comment(db.Model):
    """Comment"""

    id: int = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
    )

    name: str = db.Column(Unicode(const.NAME_SIZE))
    website: t.Optional[str] = db.Column(db.String(const.WEBSITE_SIZE), nullable=True)

    email_ct: bytes = db.Column(db.LargeBinary(length=const.EMAIL_CT_SIZE))
    key: bytes = db.Column(db.LargeBinary(length=32))

    comment: str = db.Column(Unicode(const.COMMENT_SIZE))
    confirmed: bool = db.Column(db.Boolean, default=False)
    posted: datetime.datetime = db.Column(DateTime, nullable=False)

    token: str = db.Column(db.String(32))

    def __init__(
        self, name: str, website: t.Optional[str], email: str, comment: str
    ) -> None:
        assert len(name) <= const.NAME_SIZE, "Name too long"
        assert len(website or "") <= const.WEBSITE_SIZE, "Website too long"
        assert len(email) <= const.EMAIL_CT_SIZE, "Email too long"
        assert len(comment) <= const.COMMENT_SIZE, "Comment too long"

        self.name: str = name
        self.website: t.Optional[str] = website

        self.key: bytes = rand.randbytes(32)
        self.email_ct: bytes = crc4.rc4(self.email.encode(), self.key)  # type: ignore

        self.comment: str = comment
        self.confirmed: bool = False
        self.posted: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)

        self.token: str = "".join(
            rand.choices(string.ascii_letters + string.digits, k=32)
        )

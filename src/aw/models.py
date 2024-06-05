#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DB Models"""

import typing as t
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DECIMAL, Dialect, TypeDecorator

from . import const

db: SQLAlchemy = SQLAlchemy()


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
        primary_key=True,
        unique=True,
    )
    count: int = db.Column(HugeUInt())

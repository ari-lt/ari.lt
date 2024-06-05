#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""routing"""

from typing import Any

from flask import Blueprint


class Bp(Blueprint):
    def get(self, rule: str, **kwargs: Any) -> Any:
        """wrapper for GET"""
        return self.route(rule=rule, methods=("GET",), **kwargs)

    def post(self, rule: str, **kwargs: Any) -> Any:
        """wrapper for POST"""
        return self.route(rule=rule, methods=("POST",), **kwargs)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""limiter"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter: Limiter = Limiter(
    get_remote_address,
    default_limits=["10000 per day", "1500 per hour", "50 per minute"],
    storage_uri="memory://",
)

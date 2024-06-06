#!/bin/sh

set -u

main() {
    kill -9 $(pgrep python3) || true
    kill -9 $(pgrep memcached) || true

    cd src
    python3 -m pip install gunicorn
    python3 -m gunicorn -b 127.0.0.1:17312 -w 1 main:app &
}

main "$@"

#!/usr/bin/env sh

set -eu

main() {
    gpg --detach-sign --armor index.html
    gpg --verify index.html.asc
}

main "$@"

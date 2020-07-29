#!/bin/sh

BASE_DIR="$(dirname -- "`readlink -f -- "$0"`")"

cd -- "$BASE_DIR"
set -e

if [ ! -x ./caddy ]; then
    export VERSION="2.1.1"
    wget -O caddy.tar.gz "https://github.com/caddyserver/caddy/releases/download/v${VERSION}/caddy_${VERSION}_linux_amd64.tar.gz"
    tar xzf caddy.tar.gz
    rm caddy.tar.gz
fi

./caddy start -config Caddyfile
python server.py

#!/usr/bin/env sh
$(dirname $(readlink -f $0))/.venv/bin/gunicorn \
-c gunicorn.conf.py

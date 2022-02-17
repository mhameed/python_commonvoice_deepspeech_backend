#!/usr/bin/env sh
export PROMETHEUS_MULTIPROC_DIR=$(mktemp  -d '/tmp/prometheus_flask_exporter_XXX')
$(dirname $(readlink -f $0))/.venv/bin/gunicorn \
-c gunicorn.conf.py

#!/usr/bin/env sh
# Load variables into the environment, and start waitress
. $(dirname $(readlink -f $0))/setenv.sh
$(dirname $(readlink -f $0))/mywaitress.py

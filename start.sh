#!/usr/bin/env sh
# activate virtualenv
. $(dirname $(readlink -f $0))/.venv/bin/activate
# Load variables into the environment, and start waitress
. $(dirname $(readlink -f $0))/setenv.sh
$(dirname $(readlink -f $0))/mywaitress.py

#!/usr/bin/env ash
# Load variables into the environment, and start waitress
source $(dirname $(readlink -f $0))/setenv.sh
$(dirname $(readlink -f $0))/mywaitress.py

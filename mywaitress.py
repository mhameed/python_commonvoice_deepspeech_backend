#!/usr/bin/env python
from os import environ as env
from waitress import serve
import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

import app
serve(app.create_app(), listen='*:'+env['serveport'], trusted_proxy='10.1.2.82', url_prefix=env['url_prefix'])

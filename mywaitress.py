#!/usr/bin/env python
import app
import logging
from os import environ as env
from paste.translogger import TransLogger
from waitress import serve

logger = logging.getLogger('cv')
logger.setLevel(logging.DEBUG)
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

logging.basicConfig(filename='cv.log', encoding='utf-8', level=logging.DEBUG)

serve(TransLogger(app.create_app(), setup_console_handler=False), listen='*:'+env['serveport'], trusted_proxy='10.1.3.83', url_prefix=env['url_prefix'])

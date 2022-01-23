#!/usr/bin/env python
from os import environ as env
from waitress import serve
from paste.translogger import TransLogger
import logging
logger = logging.getLogger('cv')
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename='cv.log', encoding='utf-8', level=logging.DEBUG)
import app
serve(TransLogger(app.create_app(), setup_console_handler=False), listen='*:'+env['serveport'], trusted_proxy='10.1.3.83', url_prefix=env['url_prefix'])

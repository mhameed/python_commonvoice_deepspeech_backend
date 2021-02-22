# -*- coding: utf-8 -*-
import json
import base64
import sys
import os
from app import db
from flask import jsonify, abort, request, make_response, url_for, render_template, Response, send_from_directory
from flask_classy import FlaskView
import markdown
from markupsafe import Markup


class DocsView(FlaskView):
    def index(self):
        return self.get('index')

    def get(self, id):
        fname = os.path.join(os.getcwd(), 'docs', id+'.md')
        with open(fname) as f:
            mdText = f.read()
        docs = Markup(markdown.markdown(mdText, encoding='utf-8'))
        html = render_template('docs_index.html', body=docs)
        r = make_response(html)
        r.mimetype = "text/html"
        return r

import uuid
import json
import sys
import os
from flask import Blueprint, g, jsonify, abort, request, make_response, url_for, render_template, Response, send_from_directory
from sqlalchemy.exc import IntegrityError
from plumbum.cmd import ffmpeg
from app import db, metrics
from ..models import Clip, Sentence, Unrecognized

ffmpeg_cmd = ffmpeg['-i', '-', '-ac', '1', '-ar', '44100', '-f', 'ogg', '-']

bp = Blueprint('unrecognized', __name__, url_prefix='/unrecognized')

metrics['cv_requests'].labels(method='post', endpoint='/', view='unrecognized')
@bp.route('', methods=['POST'])
def post():
    metrics['cv_requests'].labels(method='post', endpoint='/', view='unrecognized').inc()
    u = Unrecognized()
    u.data = (ffmpeg_cmd << request.get_data() ).popen().stdout.read()
    u.save()
    return jsonify(filePrefix=u.id)

metrics['cv_requests'].labels(method='get', endpoint='/', view='unrecognized')
@bp.route('', methods=['GET'])
def get():
    metrics['cv_requests'].labels(method='get', endpoint='/', view='unrecognized').inc()
    u = Unrecognized.query.first()
    if not u:
        return make_response(jsonify(status='No result found'), 404)
    d = {}
    d['id'] = u.id
    d['audioSrc'] = 'https://cv.hameed.info' + url_for('resources.get', id=u.id)
    return jsonify(d)

# patch method should be revised or deleted, as we now expect raw audio rather than a json object containing encoded audio.
@bp.route('', methods=['PATCH'])
def patch():
    u_id = request.headers.get('unrecognized_id')
    u = Unrecognized.query.filter(Unrecognized.id==u_id).first()
    if not u:
        return make_response(jsonify(status='No such unrecognized clip'), 404)
    content = request.json
    text = content['text']
    if not text:
        return make_response(jsonify(status='No text provided'), 400)
    s = Sentence.query.filter(Sentence.text==text).first()
    if not s:
        s = Sentence(text=text)
        s.save()
    c = Clip(sentence_id=s.id)
    c.data = u.data
    c.save()
    u.delete()
    return make_response(jsonify(status='ok, all done'), 200)

# vim: sw=4 ts=4 sts=4 expandtab

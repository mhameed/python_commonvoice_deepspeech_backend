import uuid
import json
import sys
import os
from flask import Blueprint, g, jsonify, abort, request, make_response, url_for, render_template, Response, send_from_directory
from sqlalchemy.exc import IntegrityError
from tempfile import mkstemp
from plumbum.cmd import ffmpeg, mv
from app import db
from ..models import Clip, Sentence, Unrecognized

_, tmp_fname = mkstemp(prefix='mcv_.', suffix='.mp3')
ffmpeg_cmd = ffmpeg['-i', '-', '-ac', '1', '-ar', '44100', '-y', tmp_fname]

bp = Blueprint('unrecognized', __name__, url_prefix='/unrecognized')

@bp.route('', methods=['POST'])
def post():
    u = Unrecognized()
    u.save()
    (ffmpeg_cmd << request.get_data() )()
    fname = os.path.join(os.getcwd(), 'audio', u.id+'.mp3')
    mv[tmp_fname, fname]()
    return jsonify(filePrefix=u.id)

@bp.route('', methods=['GET'])
def get():
    u = Unrecognized.query.first()
    if not u:
        return make_response(jsonify(status='No result found'), 404)
    d = {}
    d['id'] = u.id
    d['audioSrc'] = 'https://cv.hameed.info' + url_for('resources.get', id=u.id)
    return jsonify(d)

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
    c.save()
    oldname = os.path.join(os.getcwd(), 'audio', u.id+'.mp3')
    newname = os.path.join(os.getcwd(), 'audio', c.id+'.mp3')
    mv[oldname, newname]()
    u.delete()
    return make_response(jsonify(status='ok, all done'), 200)

# vim: sw=4 ts=4 sts=4 expandtab

import uuid
import json
import sys
import os
from flask import Blueprint, g, jsonify, abort, request, make_response, url_for, render_template, Response, send_from_directory
from sqlalchemy.exc import IntegrityError
from tempfile import mkstemp
from plumbum.cmd import ffmpeg, cp
from app import db
from ..models import Clip, Sentence

_, tmp_fname = mkstemp(prefix='mcv_.', suffix='.mp3')
ffmpeg_cmd = ffmpeg['-i', '-',  '-ac', '1', '-ar', '44100', '-y', tmp_fname]

bp = Blueprint('clips', __name__, url_prefix='/clips')

@bp.route('', methods=['POST'])
def post():
    sentence_id = request.headers.get('sentence_id')
    s = Sentence.query.filter(Sentence.id==sentence_id).first()
    if not s:
        return make_response(jsonify(status='No such sentence'), 404)
    c = Clip(sentence_id=sentence_id)
    c.save()
    (ffmpeg_cmd << request.get_data() )()
    fname = os.path.join(os.getcwd(), 'audio', c.id+'.mp3')
    cp[tmp_fname, fname]()
    return jsonify(filePrefix=c.id)

@bp.route('', methods=['GET'])
def get():
    count = request.args.get('count', '1')
    try:
        count = int(count)
    except:
        count = 1
    if count < 1 :
        count = 1
    elif count > 100:
        count = 100
    resp = []
    for c in  Clip.query.filter(Clip.positiveVotes+Clip.negativeVotes < 5).limit(count).all():
        d = {}
        d['id'] = c.id
        d['audioSrc'] = 'https://cv.hameed.info' + url_for('resources.get', id=c.id)
        d['glob'] = c.id+'/'+c.sentence.id
        d['sentence'] = {'id':c.sentence.id, 'text':c.sentence.text}
        resp.append(d)
    if resp is []:
        return make_response(jsonify(status='No result found'), 404)
    return jsonify(resp)

# vim: sw=4 ts=4 sts=4 expandtab

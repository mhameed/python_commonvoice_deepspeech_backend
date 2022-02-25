import logging
import os
import sqlalchemy as _sa
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for
from plumbum.cmd import ffmpeg, sox
from sqlalchemy.exc import IntegrityError
from tempfile import mkstemp
from app import db
from ..models import Clip, Sentence, Unrecognized

logger = logging.getLogger('cv.unrecognized')

bp = Blueprint('unrecognized', __name__, url_prefix='/unrecognized')

@bp.route('', methods=['POST'])
def post():
    if not request.content_type.lower().startswith('audio/'):
        return make_response(jsonify(status='Expected "content-type: audio/*" header'), 400)
    u = Unrecognized(user=g.user, language=g.language)
    _, tmp_fname1 = mkstemp(prefix='ds_unrecognized_', suffix='.wav')
    _, tmp_fname2 = mkstemp(prefix='ds_unrecognized_', suffix='.wav')
    _, tmp_fname3 = mkstemp(prefix='ds_unrecognized_', suffix='.ogg')
    ffmpeg_in = ffmpeg['-i', '-', '-ac', '1', '-ar', '44100', '-y', tmp_fname1]
    sox_mid = sox[tmp_fname1, tmp_fname2, 'norm', '-0.1']
    ffmpeg_out = ffmpeg['-i', tmp_fname2, '-y', tmp_fname3]
    (ffmpeg_in << request.get_data() )()
    sox_mid()
    ffmpeg_out()
    with open(tmp_fname3, 'rb') as f:
        u.data = f.read()
    os.remove(tmp_fname1)
    os.remove(tmp_fname2)
    os.remove(tmp_fname3)
    u.save()
    return jsonify(filePrefix=u.id)

@bp.route('', methods=['GET'])
def get():
    u = Unrecognized.query.filter(_sa.and_(Unrecognized.user==g.user, Unrecognized.language==g.language)).first()
    if not u:
        return make_response(jsonify([]), 404)
    d = {}
    d['id'] = u.id
    d['audioSrc'] = request.url_root + url_for('resources.get', id=u.id, language=g.language, user=g.user)
    return jsonify(d)

# vim: sw=4 ts=4 sts=4 expandtab

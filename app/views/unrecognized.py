import logging
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for
from sqlalchemy.exc import IntegrityError
from plumbum.cmd import ffmpeg
from app import db, metrics
from ..models import Clip, Sentence, Unrecognized

ffmpeg_cmd = ffmpeg['-i', '-', '-ac', '1', '-ar', '44100', '-f', 'ogg', '-']
logger = logging.getLogger('cv.unrecognized')

bp = Blueprint('unrecognized', __name__, url_prefix='/unrecognized')

metrics['cv_requests'].labels(method='post', endpoint='/', view='unrecognized')
@bp.route('', methods=['POST'])
def post():
    metrics['cv_requests'].labels(method='post', endpoint='/', view='unrecognized').inc()
    if not request.content_type.lower().startswith('audio/'):
        return make_response(jsonify(status='Expected "content-type: audio/*" header'), 400)
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
        return make_response(jsonify(status='No unrecognized audio clips.'), 404)
    d = {}
    d['id'] = u.id
    d['audioSrc'] = 'https://cv.hameed.info' + url_for('resources.get', id=u.id, language=g.language, user=g.user)
    return jsonify(d)

# vim: sw=4 ts=4 sts=4 expandtab

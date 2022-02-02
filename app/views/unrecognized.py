import logging
import sqlalchemy as _sa
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for
from prometheus_client import Counter
from sqlalchemy.exc import IntegrityError
from plumbum.cmd import ffmpeg
from app import db, getMetric
from ..models import Clip, Sentence, Unrecognized

ffmpeg_cmd = ffmpeg['-i', '-', '-ac', '1', '-ar', '44100', '-f', 'ogg', '-']
logger = logging.getLogger('cv.unrecognized')

bp = Blueprint('unrecognized', __name__, url_prefix='/unrecognized')

@bp.route('', methods=['POST'])
def post():
    metric = getMetric(
        name='commonvoice_requests',
        typ=Counter,
        labels={'method':request.method,
            'endpoint': url_for(request.endpoint, language=g.language, user=g.user)
        }
    )
    metric.inc()

    if not request.content_type.lower().startswith('audio/'):
        return make_response(jsonify(status='Expected "content-type: audio/*" header'), 400)
    u = Unrecognized(user=g.user, language=g.language)
    u.data = (ffmpeg_cmd << request.get_data() ).popen().stdout.read()
    u.save()
    return jsonify(filePrefix=u.id)

@bp.route('', methods=['GET'])
def get():
    metric = getMetric(
        name='commonvoice_requests',
        typ=Counter,
        labels={'method':request.method,
            'endpoint': url_for(request.endpoint, language=g.language, user=g.user)
        }
    )
    metric.inc()

    u = Unrecognized.query.filter(_sa.and_(Unrecognized.user==g.user, Unrecognized.language==g.language)).first()
    if not u:
        return make_response(jsonify(status='No unrecognized audio clips.'), 404)
    d = {}
    d['id'] = u.id
    d['audioSrc'] = 'https://cv.hameed.info' + url_for('resources.get', id=u.id, language=g.language, user=g.user)
    return jsonify(d)

# vim: sw=4 ts=4 sts=4 expandtab

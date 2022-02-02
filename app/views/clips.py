import json
import logging
import sqlalchemy as _sa
import urllib
from app import db, getMetric
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for 
from plumbum.cmd import ffmpeg
from prometheus_client import Counter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from ..models import Clip, Sentence

logger = logging.getLogger('cv.clips')

ffmpeg_cmd = ffmpeg['-i', '-', '-ac', '1', '-ar', '44100', '-f', 'ogg', '-']

bp = Blueprint('clips', __name__, url_prefix='/clips')

@bp.route('/<id>/votes', methods=['POST'])
def vote(id):
    metric = getMetric(
        name='commonvoice_requests',
        typ=Counter,
        labels={'method':request.method,
            'endpoint': url_for(request.endpoint, language=g.language, user=g.user, id=id)
        }
    )
    metric.inc()

    logger.debug(f"vote: received an id of:{id}")
    c = Clip.query.filter(Clip.id==id).first()
    if not c:
        logger.debug(f"vote: no such id:{id}, returning")
        return make_response(jsonify(status='No such clip'), 404)
    logger.debug(f"vote: with id:{id}, its associated string is {c.sentence.text}")
    content = request.json
    if content['isValid']:
        c.positiveVotes += 1
        logger.debug(f"vote: clipid:{id} positive incremented")
    else:
        c.negativeVotes += 1
        logger.debug(f"vote: clipid:{id} negative incremented")
    c.save()
    return jsonify(glob=c.id+'/'+c.sentence.id)

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
    sentence_id = request.headers.get('sentence_id')
    if sentence_id:
        logger.debug(f"post: received header with sentence_id:{sentence_id}")
        s = Sentence.query.filter(_sa.and_(Sentence.id==sentence_id, Sentence.user==g.user, Sentence.language==g.language)).first()
    else:
        sentence = urllib.parse.unquote(request.headers.get('sentence'))
        logger.debug(f"post: received header with sentence:{sentence}")
        s = Sentence.query.filter(_sa.and_(Sentence.user==g.user, Sentence.language==g.language, Sentence.text==sentence)).first()
    if not s:
        logger.debug(f"post: could not find a sentence with text:{sentence} or id:{sentence_id}")
        return make_response(jsonify(status='No such sentence', sentence_id=sentence_id, sentence=sentence), 404)
    c = Clip(sentence_id=s.id, language=g.language, user=g.user)
    c.data = (ffmpeg_cmd << request.get_data() ).popen().stdout.read()
    c.save()
    logger.debug(f"post: associating {c.id} with {s.id}, which has a text of {s.text}")
    return jsonify(filePrefix=c.id)

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
    voteTotal = 0
    while voteTotal<6:
        for c in  Clip.query.filter(_sa.and_(Clip.user==g.user, Clip.language==g.language, Clip.positiveVotes+Clip.negativeVotes == voteTotal)).order_by(func.random()).limit(count):
            d = {}
            d['id'] = c.id
            d['audioSrc'] = 'https://cv.hameed.info' + url_for('resources.get', id=c.id, language=g.language, user=g.user)
            d['glob'] = c.id+'/'+c.sentence.id
            d['sentence'] = {'id':c.sentence.id, 'text':c.sentence.text}
            resp.append(d)
        voteTotal += 1
        if len(resp) == count:
            break
    if resp is []:
        logger.debug("get: returning []")
        return make_response(jsonify(resp), 404)
    logger.debug("get: returning %s\n", json.dumps(resp))
    return jsonify(resp)

# vim: sw=4 ts=4 sts=4 expandtab

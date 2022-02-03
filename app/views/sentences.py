import logging
import sqlalchemy as _sa
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for
from prometheus_client import Counter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from app import db, getMetric
from ..models import Sentence

logger = logging.getLogger('cv.sentences')

bp = Blueprint('sentences', __name__, url_prefix='/sentences')

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
    logger.debug(f"get: Received a request count:{count}")
    resp = []
    for s in Sentence.query.filter(_sa.and_(Sentence.user==g.user, Sentence.language==g.language)).order_by(func.random()):
        if len(s.clips) > 1: continue
        resp.append(s.to_dict())
        if len(resp) == count: break
    if resp is []:
        logger.debug(f"get: returning {resp}")
        return make_response(jsonify(resp), 404)
    logger.debug(f"get: returning {resp}")
    return jsonify(resp)

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

    content = request.json
    text = content['text']
    if not text:
        return make_response(jsonify(status='No text provided'), 400)
    entry = Sentence(text=text, language=g.language, user=g.user, source=content.get('source', ''))
    try:
        entry.save()
    except IntegrityError:
        return make_response(jsonify(status='Duplicate entry'), 400)
    return jsonify(id=entry.id, text=text, source=content.get('source', ''))

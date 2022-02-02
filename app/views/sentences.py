import logging
import sqlalchemy as _sa
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from app import db, metrics
from ..models import Sentence

logger = logging.getLogger('cv.sentences')

bp = Blueprint('sentences', __name__, url_prefix='/sentences')

metrics['cv_requests'].labels(method='get', endpoint='/', view='sentences')
@bp.route('', methods=['GET'])
def get():
    metrics['cv_requests'].labels(method='get', endpoint='/', view='sentences').inc()
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
        return make_response(jsonify(status='No result found'), 404)
    logger.debug(f"get: returning {resp}")
    return jsonify(resp)

metrics['cv_requests'].labels(method='post', endpoint='/', view='sentences')
@bp.route('', methods=['POST'])
def post():
    metrics['cv_requests'].labels(method='post', endpoint='/', view='sentences').inc()
    content = request.json
    text = content['text']
    if not text:
        return make_response(jsonify(status='No text provided'), 400)
    entry = Sentence(text=text, language=g.language, user=g.user)
    try:
        entry.save()
    except IntegrityError:
        return make_response(jsonify(status='Duplicate entry'), 400)
    return jsonify(id=entry.id, text=text)

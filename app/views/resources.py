import logging
import sqlalchemy as _sa
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for
from prometheus_client import Counter
from sqlalchemy.exc import IntegrityError
from app import db, getMetric
from ..models import Clip

logger = logging.getLogger('cv.resources')

bp = Blueprint('resources', __name__, url_prefix='/resources')
@bp.route('/<id>', methods=['GET'])
def get(id):
    metric = getMetric(
        name='commonvoice_requests',
        typ=Counter,
        labels={'method':request.method,
            'endpoint': url_for(request.endpoint, language=g.language, user=g.user, id=id)
        }
    )
    metric.inc()

    logger.debug(f"get: Received a request with id:{id}")
    if id.startswith('Unrecognized'):
        u = Unrecognized.query.filter(_sa.and_(Unrecognized.user==g.user, Unrecognized.language==g.language, Unrecognized.id==id)).first()
        return Response(u.data, mimetype='audio/ogg')
    elif id.startswith('Clip'):
        c = Clip.query.filter(_sa.and_(Clip.user==g.user, Clip.language==g.language, Clip.id==id)).first()
        return Response(c.data, mimetype='audio/ogg')
    logger.debug(f"get: Could not find resource with id:{id}")
    return make_response(jsonify(status='File not found.'), 404)

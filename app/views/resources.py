import uuid
import json
import sys
import os
from flask import Blueprint, g, jsonify, abort, request, make_response, url_for, render_template, Response
from sqlalchemy.exc import IntegrityError
from app import db, metrics
from ..models import Clip
import logging
logger = logging.getLogger('cv.resources')

bp = Blueprint('resources', __name__, url_prefix='/resources')
metrics['cv_requests'].labels(method='get', endpoint='/{id}', view='resources')
@bp.route('/<id>', methods=['GET'])
def get(id):
    # two metrics, one that includes the id, and one that has the template of the id so that we can count how many times resources itself has been called regardless of id
    metrics['cv_requests'].labels(method='get', endpoint='/{id}', view='resources').inc()
    metrics['cv_requests'].labels(method='get', endpoint=f'/{id}', view='resources').inc()
    logger.debug(f"get: Received a request with id:{id}")
    if id.startswith('Unrecognized'):
        u = Unrecognized.query.filter(Unrecognized.id==id).first()
        return Response(u.data, mimetype='audio/ogg')
    elif id.startswith('Clip'):
        c = Clip.query.filter(Clip.id==id).first()
        return Response(c.data, mimetype='audio/ogg')
    logger.debug(f"get: Could not find resource with id:{id}")
    return make_response(jsonify(status='File not found.'), 404)

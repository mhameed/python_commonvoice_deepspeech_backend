import uuid
import json
import sys
import os
from flask import Blueprint, g, jsonify, abort, request, make_response, url_for, render_template, Response
from sqlalchemy.exc import IntegrityError
from app import db
from ..models import Clip
import logging
logger = logging.getLogger('cv.resources')

bp = Blueprint('resources', __name__, url_prefix='/resources')

@bp.route('/<id>', methods=['GET'])
def get(id):
    logger.debug(f"get: Received a request with id:{id}")
    if id.startswith('u-'):
        u = Unrecognized.query.filter(Unrecognized.id==id).first()
        return Response(u.data, mimetype='audio/ogg')
    elif id.startswith('a-'):
        c = Clip.query.filter(Clip.id==id).first()
        return Response(c.data, mimetype='audio/ogg')
    logger.debug(f"get: Could not find resource with id:{id}")
    return make_response(jsonify(status='File not found.'), 404)

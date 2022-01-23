import uuid
import json
import sys
import os
from flask import Blueprint, g, jsonify, abort, request, make_response, url_for, render_template, Response, send_from_directory
from sqlalchemy.exc import IntegrityError
from  sqlalchemy.sql.expression import func
from app import db
from ..models import Sentence

bp = Blueprint('sentences', __name__, url_prefix='/sentences')

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
    for s in Sentence.query.order_by(func.random()):
        if len(s.clips) > 1: continue
        resp.append(s.to_dict())
        if len(resp) == count: break
    if resp is []:
        return make_response(jsonify(status='No result found'), 404)
    return jsonify(resp)

@bp.route('', methods=['POST'])
def post():
    content = request.json
    text = content['text']
    if not text:
        return make_response(jsonify(status='No text provided'), 400)
    entry = Sentence(text=text)
    try:
        entry.save()
    except IntegrityError:
        return make_response(jsonify(status='Duplicate entry'), 400)
    return jsonify(id=entry.id, text=text)

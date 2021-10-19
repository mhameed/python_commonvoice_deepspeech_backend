import uuid
import json
import sys
import os
from flask import Blueprint, g, jsonify, abort, request, make_response, url_for, render_template, Response, send_from_directory
from sqlalchemy.exc import IntegrityError
from app import db
from ..models import Clip, Sentence

bp = Blueprint('clips', __name__, url_prefix='/clips')

@bp.route('', methods=['POST'])
def post():
    sentence_id = request.headers.get('sentence_id')
    s = Sentence.query.filter(Sentence.id==sentence_id).first()
    if not s:
        return make_response(jsonify(status='No such sentence'), 400)
    c = Clip(sentence_id=sentence_id)
    c.save()
    with open('/tmp/%s.mp3' %c.id, 'wb') as f:
        f.write(request.get_data())
    return jsonify(filePrefix=c.id)

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
    for c in  Clip.query.filter(Clip.positiveVotes+Clip.negativeVotes < 5).limit(count).all():
        d = {}
        d['id'] = c.id
        d['audioSrc'] = 'https://cv.hameed.info' + url_for('resources.get', id=c.id)
        s = c.sentence
        d['sentence'] = {'id':s.id, 'text':s.text}
        resp.append(d)
    if resp is []:
        return make_response(jsonify(status='No result found'), 404)
    return jsonify(resp)

# vim: sw=4 ts=4 sts=4 expandtab

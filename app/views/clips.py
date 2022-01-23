import uuid
import json
import urllib
import sys
import os
from flask import Blueprint, g, jsonify, abort, request, make_response, url_for, render_template, Response, send_from_directory
from sqlalchemy.exc import IntegrityError
from  sqlalchemy.sql.expression import func
from plumbum.cmd import ffmpeg
from app import db
from ..models import Clip, Sentence
import logging
logger = logging.getLogger('cv.clips')

ffmpeg_cmd = ffmpeg['-i', '-', '-ac', '1', '-ar', '44100', '-f', 'ogg', '-']

bp = Blueprint('clips', __name__, url_prefix='/clips')

@bp.route('/<id>/votes', methods=['POST'])
def vote(id):
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
    return jsonify(status='ok')

@bp.route('', methods=['POST'])
def post():
    sentence_id = request.headers.get('sentence_id')
    if sentence_id:
        logger.debug(f"post: received header with sentence_id:{sentence_id}")
        s = Sentence.query.filter(Sentence.id==sentence_id).first()
    else:
        sentence = urllib.parse.unquote(request.headers.get('sentence'))
        logger.debug(f"post: received header with sentence:{sentence}")
        s = Sentence.query.filter(Sentence.text==sentence).first()
    if not s:
        logger.debug(f"post: could not find a sentence with text:{sentence} or id:{sentence_id}")
        return make_response(jsonify(status='No such sentence', sentence_id=sentence_id, sentence=sentence), 404)
    c = Clip(sentence_id=s.id)
    c.data = (ffmpeg_cmd << request.get_data() ).popen().stdout.read()
    c.save()
    logger.debug(f"post: associating {c.id} with {s.id}, which has a text of {s.text}")
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
    for c in  Clip.query.filter(Clip.positiveVotes+Clip.negativeVotes < 2).order_by(func.random()).limit(count):
        d = {}
        d['id'] = c.id
        d['audioSrc'] = 'https://cv.hameed.info' + url_for('resources.get', id=c.id)
        d['glob'] = c.id+'/'+c.sentence.id
        d['sentence'] = {'id':c.sentence.id, 'text':c.sentence.text}
        resp.append(d)
    if resp is []:
        logger.debug("get: returning []")
        return make_response(jsonify(status='No result found'), 404)
    logger.debug("get: returning %s\n", json.dumps(resp))
    return jsonify(resp)

# vim: sw=4 ts=4 sts=4 expandtab

import json
import logging
import os
import sqlalchemy as _sa
import urllib
from app import db 
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for 
from plumbum.cmd import ffmpeg, sox
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from tempfile import mkstemp
from ..models import Clip, Sentence

logger = logging.getLogger('cv.clips')


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
    return jsonify(glob=c.id+'/'+c.sentence.id)

@bp.route('', methods=['POST'])
def post():
    if not request.content_type.lower().startswith('audio/'):
        return make_response(jsonify(status='Expected "content-type: audio/*" header'), 400)
    sentence_id = request.headers.get('sentence-id')
    if sentence_id:
        logger.debug(f"post: received header with sentence_id:{sentence_id}")
        s = Sentence.query.filter(_sa.and_(Sentence.id==sentence_id, Sentence.user==g.user, Sentence.language==g.language)).first()
    if not s:
        logger.debug(f"post: could not find a sentence with text:{sentence} or id:{sentence_id}")
        return make_response(jsonify(status='No such sentence', sentence_id=sentence_id, sentence=sentence), 404)
    c = Clip(sentence_id=s.id, language=g.language, user=g.user)
    _, tmp_fname1 = mkstemp(prefix='ds_clip.', suffix='.wav')
    _, tmp_fname2 = mkstemp(prefix='ds_clip.', suffix='.wav')
    _, tmp_fname3 = mkstemp(prefix='ds_clip.', suffix='.ogg')
    ffmpeg_in = ffmpeg['-i', '-', '-ac', '1', '-ar', '44100', '-y', tmp_fname1]
    sox_mid = sox[tmp_fname1, tmp_fname2, 'norm', '-0.1']
    ffmpeg_out = ffmpeg['-i', tmp_fname2, '-y', tmp_fname3]
    (ffmpeg_in << request.get_data() )()
    sox_mid()
    ffmpeg_out()
    with open(tmp_fname3, 'rb') as f:
        c.data = f.read()
    os.remove(tmp_fname1)
    os.remove(tmp_fname2)
    os.remove(tmp_fname3)
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

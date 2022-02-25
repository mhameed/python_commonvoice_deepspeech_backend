import logging
import os
import sqlalchemy as _sa
import urllib
from app import db
from flask import Blueprint, g, jsonify, make_response, request, Response, url_for
from plumbum.cmd import ffmpeg, sox
from sqlalchemy.exc import IntegrityError
from tempfile import mkstemp
from ..models import Clip, Sentence, Unrecognized

logger = logging.getLogger('cv.correct')

bp = Blueprint('correct', __name__, url_prefix='/correct')

@bp.route('', methods=['POST'])
def post():
    if request.content_type.lower().startswith('audio/'):
        sentence = urllib.parse.unquote(request.headers.get('sentence', ''))
        source = urllib.parse.unquote(request.headers.get('source', ''))
        logger.debug(f"post: received header with sentence:{sentence}")
        if not sentence or sentence.isspace():
            return make_response(jsonify(status='Expected "sentence: <text>" header'), 400)
        else:
            s = Sentence.query.filter(_sa.and_(Sentence.language==g.language, Sentence.user==g.user, Sentence.text==sentence)).first()
        if not s:
            logger.debug(f"post: could not find a sentence with text:{sentence}, going to create one.")
            s = Sentence(text=sentence, language=g.language, user=g.user, source=source)
            s.save()
        c = Clip(sentence_id=s.id, language=g.language, user=g.user)
        _, tmp_fname1 = mkstemp(prefix='ds_correct_', suffix='.wav')
        _, tmp_fname2 = mkstemp(prefix='ds_correct_', suffix='.wav')
        _, tmp_fname3 = mkstemp(prefix='ds_correct_', suffix='.ogg')
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
        c.positiveVotes = 1
        c.save()
        logger.debug(f"post: associating {c.id} with {s.id}, which has a text of {s.text}")
        return jsonify(filePrefix=c.id)
    elif request.content_type.lower().startswith('application/json'):
        content = request.json
        if 'text' not in content or 'id' not in content or len(content.keys()) != 2:
            return make_response(jsonify(status='Expected "id" and "text"'), 400)
        u_id = content['id']
        u = Unrecognized.query.filter(_sa.and_(Unrecognized.language==g.language, Unrecognized.user==g.user, Unrecognized.id==u_id)).first()
        if not u:
            return make_response(jsonify(status='No such unrecognized clip'), 404)
        text = content['text']
        if not text or text.isspace():
            return make_response(jsonify(status='No text provided'), 400)
        s = Sentence.query.filter(_sa.and_(Sentence.user==g.user, Sentence.language==g.language, Sentence.text==text)).first()
        if not s:
            s = Sentence(text=text, user=g.user, language=g.language)
            s.save()
        c = Clip(sentence_id=s.id, language=g.language, user=g.user)
        c.data = u.data
        c.positiveVotes = 1
        c.save()
        u.delete()
        return make_response(jsonify(status='ok, all done'), 200)

# vim: sw=4 ts=4 sts=4 expandtab

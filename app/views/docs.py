import logging
import markdown
import os
from app import metrics
from flask import Blueprint, make_response
from markupsafe import Markup

logger = logging.getLogger('cv.docs')


bp = Blueprint('docs', __name__, url_prefix='/docs')

metrics['cv_requests'].labels(method='get', endpoint='/{id}', view='docs')
metrics['cv_requests'].labels(method='get', endpoint='/', view='docs')
@bp.route('/<id>', methods=['GET'])
@bp.route('/', methods=['GET'])
@bp.route('', methods=['GET'])
def get(id='index'):
    metrics['cv_requests'].labels(method='get', endpoint=f'/{id}', view='docs').inc()
    fname = os.path.join(os.getcwd(), 'docs', f'{id}.md')
    with open(fname) as f:
        mdText = f.read()
    docs = Markup(markdown.markdown(mdText, encoding='utf-8'))
    r = make_response(docs)
    r.mimetype = "text/html"
    return r

# vim: sw=4 ts=4 sts=4 expandtab

import logging
import markdown
import os
from app import getMetric
from flask import Blueprint, make_response, request, url_for
from markupsafe import Markup
from prometheus_client import Counter

logger = logging.getLogger('cv.docs')


bp = Blueprint('docs', __name__, url_prefix='/docs')

@bp.route('/<id>', methods=['GET'])
@bp.route('/', methods=['GET'])
@bp.route('', methods=['GET'])
def get(id='index'):
    metric = getMetric(
        name='commonvoice_requests',
        typ=Counter,
        labels={'method':request.method,
            'endpoint': url_for(request.endpoint, id=id)
        }
    )
    metric.inc()
    fname = os.path.join(os.getcwd(), 'docs', f'{id}.md')
    with open(fname) as f:
        mdText = f.read()
    docs = Markup(markdown.markdown(mdText, encoding='utf-8'))
    r = make_response(docs)
    r.mimetype = "text/html"
    return r

# vim: sw=4 ts=4 sts=4 expandtab

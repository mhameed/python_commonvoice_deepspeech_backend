from flask import Blueprint, Response
from prometheus_client import generate_latest
from app import db

bp = Blueprint('metrics', __name__, url_prefix='/metrics')

@bp.route('', methods=['GET'])
def get():
    return Response(generate_latest(), mimetype='text/plain')

# vim: sw=4 ts=4 sts=4 expandtab

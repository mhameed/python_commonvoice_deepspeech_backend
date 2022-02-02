import diceware
from flask import Flask, g, redirect, url_for
from prometheus_client import Counter
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
db = SQLAlchemy()
metrics = {}
metrics['cv_requests'] = Counter('cv_requests', 'total number and method of request for the given riew, endpoint.', ['view', 'method', 'endpoint'])

migrate = Migrate()

options = diceware.handle_options(args=["-n 10"])
def getRandomString(prefix=''):
  return prefix + diceware.get_passphrase(options)


def get_language_and_user(endpoint, values):
    g.language = values.pop('language')
    g.user = values.pop('user')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    myPrefix='/<user>/api/v1/<language>'
    from .views.clips import bp as clips_bp
    clips_bp.url_value_preprocessor(get_language_and_user)
    app.register_blueprint(clips_bp, url_prefix=myPrefix+clips_bp.url_prefix)
    from .views.correct import bp as correct_bp
    correct_bp.url_value_preprocessor(get_language_and_user)
    app.register_blueprint(correct_bp, url_prefix=myPrefix+correct_bp.url_prefix)
    from .views.docs import bp as docs_bp
    app.register_blueprint(docs_bp, url_prefix=docs_bp.url_prefix)
    from .views.metrics import bp as metrics_bp
    app.register_blueprint(metrics_bp, url_prefix=metrics_bp.url_prefix)
    from .views.resources import bp as resources_bp
    resources_bp.url_value_preprocessor(get_language_and_user)
    app.register_blueprint(resources_bp, url_prefix=myPrefix+resources_bp.url_prefix)
    from .views.sentences import bp as sentences_bp
    sentences_bp.url_value_preprocessor(get_language_and_user)
    app.register_blueprint(sentences_bp, url_prefix=myPrefix+sentences_bp.url_prefix)
    from .views.transcribe import bp as transcribe_bp
    transcribe_bp.url_value_preprocessor(get_language_and_user)
    app.register_blueprint(transcribe_bp, url_prefix=myPrefix+transcribe_bp.url_prefix)
    from .views.unrecognized import bp as unrecognized_bp
    unrecognized_bp.url_value_preprocessor(get_language_and_user)
    app.register_blueprint(unrecognized_bp, url_prefix=myPrefix+unrecognized_bp.url_prefix)
    print(app.url_map)
    return app

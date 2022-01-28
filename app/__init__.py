from flask import Flask, redirect, url_for
from prometheus_client import Counter
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
db = SQLAlchemy()
metrics = {}
metrics['cv_requests'] = Counter('cv_requests', 'total number and method of request for the given riew, endpoint.', ['view', 'method', 'endpoint'])

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    myPrefix='/api/v1/en'
    from .views.clips import bp as clips_bp
    app.register_blueprint(clips_bp, url_prefix=myPrefix+clips_bp.url_prefix)
    from .views.metrics import bp as metrics_bp
    app.register_blueprint(metrics_bp, url_prefix=metrics_bp.url_prefix)
    from .views.resources import bp as resources_bp
    app.register_blueprint(resources_bp, url_prefix=myPrefix+resources_bp.url_prefix)
    from .views.sentences import bp as sentences_bp
    app.register_blueprint(sentences_bp, url_prefix=myPrefix+sentences_bp.url_prefix)
    from .views.unrecognized import bp as unrecognized_bp
    app.register_blueprint(unrecognized_bp, url_prefix=myPrefix+unrecognized_bp.url_prefix)
    print(app.url_map)
    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import documentation, snippets, transcriber
    documentation.DocsView.register(app)
    snippets.SnippetsView.register(app)
    snippets.LogsView.register(app)
    transcriber.TranscriberView.register(app)
    return app

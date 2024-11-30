from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Charger la configuration à partir de `config.py`
    app.config.from_object('app.config.Config')
    CORS(app, resources={r"/*": {"origins": "*"}})
    # Initialiser les extensions (comme SQLAlchemy)
    db.init_app(app)
    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
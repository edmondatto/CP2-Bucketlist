from flask import Flask
from instance.config import app_config
from .authentication.views import auth
from .bucketlists.views import bucketlists, db
from .restplus import api


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api.add_namespace(auth)
    api.init_app(app)
    return app

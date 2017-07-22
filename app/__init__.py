from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from .auth_endpoints import auth
from .bucketlists_endpoints import bucketlists, db
from .restplus import api


# db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api.add_namespace(bucketlists)
    api.add_namespace(auth)
    api.init_app(app)
    return app

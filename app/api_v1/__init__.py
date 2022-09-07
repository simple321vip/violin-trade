from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, users, comments, errors


def create_app(config_name):
    print("")
    # ...
    # from .api_v1 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

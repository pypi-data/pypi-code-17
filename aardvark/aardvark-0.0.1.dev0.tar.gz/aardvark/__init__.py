from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os.path

db = SQLAlchemy()

from aardvark.view import mod as advisor_bp  # noqa

BLUEPRINTS = [
    advisor_bp
]

API_VERSION = '1'


def create_app(config=None):
    app = Flask(__name__, static_url_path='/static')

    if config:
        app.config.from_pyfile(config)
    else:
        if os.path.isfile('config.py'):
            app.config.from_pyfile('../config.py')
        else:
            print('No config')
            app.config.from_pyfile('_config.py')

    # For ELB and/or Eureka
    @app.route('/healthcheck')
    def healthcheck():
        return 'ok'

    # Blueprints
    for bp in BLUEPRINTS:
        app.register_blueprint(bp, url_prefix="/api/{0}".format(API_VERSION))

    # Extensions:
    db.init_app(app)

    return app

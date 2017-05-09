"""
deliverybot_patches/app.py
~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds functionality to the Flask app
"""
import types
from flask_sqlalchemy import SQLAlchemy


def _config(app, database_settings):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_setting['uri']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def _register_models(self, database, database_settings):
    _config(self, database_settings)
    database.db = SQLAlchemy(self)


def deliverybot_app(app):
    app.register_models = types.MethodType(_register_models, app)
    return app


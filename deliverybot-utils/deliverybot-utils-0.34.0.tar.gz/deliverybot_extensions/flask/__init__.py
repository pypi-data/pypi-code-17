"""
deliverybot_extensions/flask/__init__.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds behavior to the Flask app
"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from . import meta


class DeliverybotFlask(Flask):
    """
    Class that adds useful behavior
    """
    def __init__(self, name):
        super().__init__(name)
        self.register_blueprint(meta.blueprint)

    def _config_database(self, database_settings):
        self.config['SQLALCHEMY_DATABASE_URI'] = database_setting['uri']
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def register_models(self, database, database_settings):
        self._config_database(database_settings)
        database.db = SQLAlchemy(self)

"""
deliverybot_extensions/flask.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds behavior to the Flask app
"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


class DeliverybotFlask(Flask):
    """
    Class that adds useful behavior
    """
    def _config_database(self, database_settings):
        self.config['SQLALCHEMY_DATABASE_URI'] = database_setting['uri']
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def register_models(self, database, database_settings):
        self._config_database(database_settings)
        database.db = SQLAlchemy(self)

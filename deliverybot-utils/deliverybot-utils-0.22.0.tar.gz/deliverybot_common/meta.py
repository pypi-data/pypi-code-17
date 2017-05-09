"""
deliverybot_common/meta.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module exports a blueprint containing the meta endpoints
"""
from flask import Blueprint
from flask_restful import Api, Resource

blueprint = Blueprint('meta', __name__)
meta = Api(blueprint)


class HealthCheck(Resource):
    def get(self):
        return {'message': "I'm alive and breathing!"}


meta.add_resource(HealthCheck, '/healthcheck')

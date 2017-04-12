from flask import abort, jsonify
from aardvark.model import AWSIAMObject
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
import better_exceptions  # noqa
import re


mod = Blueprint('advisor', __name__)
api = Api(mod)


class RoleGet(Resource):
    """
    Get item by id
    """
    def get(self, item_id):
        item = AWSIAMObject.query.filter(AWSIAMObject.id == item_id).scalar()
        if not item:
            abort(404)

        values = []
        for advisor_data in item.usage:
            values.append(dict(
                lastAuthenticated=advisor_data.lastAuthenticated,
                serviceName=advisor_data.serviceName,
                serviceNamespace=advisor_data.serviceNamespace
            ))

        return jsonify({item.arn: values})


class RoleSearch(Resource):
    """
    Search for roles by phrase, regex, or by ARN.
    """
    def __init__(self):
        super(RoleSearch, self).__init__()
        self.reqparse = reqparse.RequestParser()

    def get(self):
        self.reqparse.add_argument('page', type=int, default=1, location='args')
        self.reqparse.add_argument('count', type=int, default=30, location='args')
        self.reqparse.add_argument('phrase', type=str, default=None, location='args')
        self.reqparse.add_argument('regex', type=str, default=None, location='args')
        self.reqparse.add_argument('arn', type=str, default=None, location='args', action='append')
        args = self.reqparse.parse_args()
        page = args.pop('page')
        count = args.pop('count')
        phrase = args.pop('phrase', '')
        arns = args.pop('arn', [])
        regex = args.pop('regex', '')

        items = None

        if phrase:
            query = AWSIAMObject.query.filter(AWSIAMObject.arn.ilike('%'+phrase+'%'))

        if arns:
            query = AWSIAMObject.query.filter(AWSIAMObject.arn.in_(arns))

        # if regex:
        #     regex = re.compile(regex)
        #     all_items = AWSIAMObject.query.all()
        #     for item in all_items:
        #         if regex.match(item.arn):
        #             items.append(item)
        if regex:
            regex = re.compile(regex)
            query = AWSIAMObject.query.filter(AWSIAMObject.arn.regexp(regex))

        items = query.paginate(page, count)

        if not items:
            items = AWSIAMObject.query.paginate(page, count)

        values = dict(page=items.page, total=items.total, count=len(items.items))
        for item in items.items:
            item_values = []
            for advisor_data in item.usage:
                item_values.append(dict(
                    lastAuthenticated=advisor_data.lastAuthenticated,
                    serviceName=advisor_data.serviceName,
                    serviceNamespace=advisor_data.serviceNamespace
                ))
            values[item.arn] = item_values

        return jsonify(values)


api.add_resource(RoleGet, '/advisor/<int:item_id>')
api.add_resource(RoleSearch, '/advisors')
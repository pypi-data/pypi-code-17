from ahqapiclient.resources import Resource


class Reports(Resource):

    def __init__(self, http_client):
        super(Reports, self).__init__('/reports', http_client)

    def create_report(self, report_type, value):
        if type(value) != unicode:
            value = unicode(value, encoding='utf-8')

        return self.post(
            path=self.rurl(report_type),
            data={'value': value}
        )

from ppg_common.base import BaseClient


class ButtercupClient(BaseClient):
    """
    ButtercupClient class-Sesion service, it has 3 routes for 3 available 
    actions.
    Services need to provide their session id while creating client object
    """
    urls = {
        "validate": "/v0/sessions/actions/validate",
        "open": "/v0/sessions/actions/open",
        "delete": "/v0/sessions/actions/delete/{}"
    }

    def __init__(self, host, port, ssl=False, session=None):
        super(ButtercupClient, self).__init__(host, port, ssl, session)

    def validate_session(self, x_session):
        """
        Method for validating session provided with parameter
        :param x_session: 
        :return:  request response
        """
        return self.get(self.urls['validate'], headers={
            "x-session": x_session
        })

    def open_session(self, user_id, user_type):
        """
        Method for opening new sessions, servive session id is provided 
        while creating object, and user_id and user_type is provided with 
        parameters in mehtod
        :param user_id: ID of user who needs new session
        :param user_type: user,task 
        :return:  request response
        """
        body = {
            "user_id": user_id, "type": user_type
        }
        return self.post(self.urls['open'], body)

    def delete_session(self, session_id):
        """
        Method for delete session with provided session_id, client object 
        needs to be created with service session i d
        :param session_id: 
        :return: request response
        """
        return self.delete(self.urls['delete'].format(session_id))


if __name__ == "__main__":
    b = ButtercupClient('localhost', '8888',
                        session='40774a50-2222-4966-a589-5132b9ab9be8')

    resp = b.open_session('f820543d-373f-7777-5555-5cfdf2e8cb4b', 'user')
    print(resp)

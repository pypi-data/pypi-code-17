from ppg_common.clients.base import BaseClient


class ButtercupClient(BaseClient):
    """
    ButtercupClient class-Sesion service, it has 3 routes for 3 available 
    actions.
    Services need to provide their session id while creating client object
    """
    urls = {
        "validate": BaseClient.version + "/sessions/actions/validate",
        "open": BaseClient.version + "/sessions/actions/open",
        "delete": BaseClient.version + "/sessions/actions/delete/{}"
    }

    def __init__(self, host, port, ssl=False, session=None):
        super(ButtercupClient, self).__init__(host, port, ssl, session)
        self.session = session

    def validate_session(self):
        """
        Method for validating session provided with parameter
        :param x_session: 
        :return:  request response
        """

        return self.get(self.urls['validate'], headers={
            "x-session": self.session
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

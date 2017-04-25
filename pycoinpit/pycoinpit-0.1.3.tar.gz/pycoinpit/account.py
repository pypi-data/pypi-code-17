import crypto


class Account(object):
    def __init__(self, private_key, server_public_key):
        self.private_key = private_key
        self.public_key = crypto.get_pub_key(self.private_key)
        self.network_code = crypto.get_network_code(self.private_key)
        self.user_id = crypto.get_user_id(self.public_key, self.network_code)
        self.server_pub_key = server_public_key
        self.shared_secret = crypto.get_shared_secret(self.server_pub_key, self.private_key)

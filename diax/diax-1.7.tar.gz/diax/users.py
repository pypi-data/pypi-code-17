class UserNotFound(Exception):
    pass

def get(client, user):
    "Get information on the user provided an email, a URI, etc"
    if user.startswith('http'):
        return client.rawget(user)
    result = client.list('users', '/users/', {'username': user})
    if len(result) == 0:
        result = client.list('users', '/users/', {'email': user})
        if len(result) == 0:
            raise UserNotFound("Could not find a user with username or email '{}'".format(user))
        return None
    elif len(result) == 1:
        return result[0]
    else:
        raise Exception("Didn't expect to get more than one user with username '{}'".format(user))

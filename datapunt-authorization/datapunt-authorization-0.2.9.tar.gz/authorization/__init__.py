"""
    authorization
    ~~~~~~~~~~~~~

    This package provides an implementation of the Datapunt authorization
    model.
"""


def authz_mapper(**psycopg2conf):
    """ Returns a function that gets a given user's authorization
    level.

    This is a convenient wrapper around an :class:`authz.map.AuthzMap` for
    callers that only want to get an authorization level for a given user, even
    if that user isn't present in the authz table (in which case it will return
    :data:`authorization_levels.LEVEL_DEFAULT`).

    Example usage:

    ::

        mapper, validator = authz.authz_mapper(psycopg2conf)
        mapper('username')  # => returns username's authz level
        validator('john@example.com', 'password')  # => returns True if password is correct, otherwise false

    :param psycopg2conf: See :function:`psycopg2.connect`
    :return: One of LEVEL_* defined in :module:`authorization_levels`
    """
    from .map import AuthzMap
    import authorization_levels

    authzmap = AuthzMap(**psycopg2conf)

    def getter(email):
        default_level = (email and authorization_levels.LEVEL_EMPLOYEE) or authorization_levels.LEVEL_DEFAULT
        return authzmap.get(email, default_level)

    def validator(email, password):
        try:
            retval = authzmap.verify_password(email, password)
        except KeyError:
            return False
        return retval

    return getter, validator

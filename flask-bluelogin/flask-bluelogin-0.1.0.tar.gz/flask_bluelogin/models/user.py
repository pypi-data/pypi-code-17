# coding: utf-8
from .base_model_ import Model
from .users import Users


class User(Model):
    def __init__(self, id=None, password=None, groups=[], properties={}):
        """
        User 

        :param id: The id of this User.
        :type id: str
        :param groups: list of group of this User.
        :type groups: list
        :param properties: dict of properties of this User.
        :type properties: dict
        :param password: password of this User.
        :type password: str
        """
        self._id = id
        self._password = password
        self._groups = groups
        self._properties = properties

    @property
    def id(self):
        """
        Gets the id of this User.
        id of user

        :return: The id of this User.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this User.
        id of user

        :param id: The id of this User.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")
        self._id = id

    @property
    def groups(self):
        """
        Gets list of group of this User.
        list of group of user

        :return: The list of group of this User.
        :rtype: list
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """
        Sets the list of group of this User.
        list of group of user

        :param level: The list of group of this User.
        :type level: list
        """
        self._groups = groups    

    @property
    def properties(self):
        """
        Gets dict of properties of this User.
        list of group of user

        :return: The dict of properties of this User.
        :rtype: dict
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets dict of properties of this User.
        dict of properties of user

        :param properties: The dict of properties of this User.
        :type properties: dict
        """
        self._properties= properties    

    @property
    def password(self):
        """
        No Gets password of this User.
        not security

        :return: None.
        :rtype: None
        """
        return None


    @password.setter
    def password(self, password):
        """
        Sets the password of this User.
        password of user

        :param password: The password of this User.
        :type password: str
        """
        if not password:
            raise ValueError("Invalid value for `password`, must not be `%s`" % password)
        self._password = password

    @property
    def is_authenticated(self):
            return True
    
    @property
    def is_active(self):
            return True
    
    @property
    def is_anonymous(self):
            return False

    def get_id(self):
            return self.id

    def in_groups(self, *groups):
        """
        Check user belongs to the groups

        :param groups: group to check
        :type groups: str
        :return: Boolean
        :rtype: bool
        """
        for group in groups:
            if group in self.groups:
                return True
        return False

    def check_password(self, password):
        """
        Check password of user

        :param password: password to check
        :type password: str
        :return: Boolean
        :rtype: bool
        """
        return Users().check_password(self, password)

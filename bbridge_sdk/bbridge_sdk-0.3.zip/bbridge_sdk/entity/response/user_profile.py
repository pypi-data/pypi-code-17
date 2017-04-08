from .bbridge_entity import BBridgeEntity
from ..enum import *


class UserProfile(BBridgeEntity):
    def __init__(self, profiling):
        """
        :type profiling: bbridge_sdk.entity.response.user_profile.UserAttributes
        """
        self.__profiling = profiling

    @classmethod
    def from_json(cls, json_object):
        return UserProfile(UserAttributes.from_json(json_object["profiling"]))

    @property
    def profiling(self):
        return self.__profiling


class UserAttributes(BBridgeEntity):
    def __init__(self, gender=None, age_group=None, relationship=None, education_level=None, income=None,
                 occupation=None):
        """
        :type gender: str | None
        :type age_group: str | None
        :type relationship: str | None
        :type education_level: str | None
        :type income: str | None
        :type occupation: str | None
        """
        self.__gender = gender
        self.__age_group = age_group
        self.__relationship = relationship
        self.__education_level = education_level
        self.__income = income
        self.__occupation = occupation

    @classmethod
    def from_json(cls, json_object):
        return UserAttributes(json_object.get(GENDER),
                              json_object.get(AGE_GROUP),
                              json_object.get(RELATIONSHIP),
                              json_object.get(EDUCATION_LEVEL),
                              json_object.get(INCOME),
                              json_object.get(OCCUPATION))

    @property
    def gender(self):
        return self.__gender

    @property
    def age_group(self):
        return self.__age_group

    @property
    def relationship(self):
        return self.__relationship

    @property
    def education_level(self):
        return self.__education_level

    @property
    def income(self):
        return self.__income

    @property
    def occupation(self):
        return self.__occupation

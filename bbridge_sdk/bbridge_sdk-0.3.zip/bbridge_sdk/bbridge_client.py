import json

import requests

from .entity import Response
from .entity.response import RequestId, BBridgeEntity
from .entity.serialize import BBridgeJSONEncoder

DEFAULT_HOST_URL = "http://bbridgeapi.cloudapp.net/v1"


class BBridgeClient(object):
    __response_url = "{}/response".format(DEFAULT_HOST_URL)

    __personal_profiling_url = "{}/profiling/personal".format(DEFAULT_HOST_URL)

    __image_objects_url = "{}/image/objects".format(DEFAULT_HOST_URL)
    __image_concepts_url = "{}/image/concepts".format(DEFAULT_HOST_URL)

    __pos_tagging_url = "{}/nlp/pos".format(DEFAULT_HOST_URL)
    __sentiment_analysis_url = "{}/nlp/sentiment".format(DEFAULT_HOST_URL)
    __name_entity_recognition_url = "{}/nlp/ner".format(DEFAULT_HOST_URL)

    @staticmethod
    def __process_response(response):
        """
        :type response: requests.Response
        :rtype: bbridge_sdk.entity.response_wrapper.Response
        """
        if response.status_code == 202:
            return Response(response.status_code, RequestId.from_json_str(response.text))
        else:
            return Response(response.status_code, err_message=response.reason)

    def __init__(self, token, host_url="http://bbridgeapi.cloudapp.net/v1"):
        """
        :type token: str
        :type host_url: str
        """
        self.__headers = {"Content-type": "application/json", "Authorization": token}

        self.__response_url = "{}/response".format(host_url)

        self.__personal_profiling_url = "{}/profiling/personal".format(host_url)

        self.__image_objects_url = "{}/image/objects".format(host_url)
        self.__image_concepts_url = "{}/image/concepts".format(host_url)

        self.__pos_tagging_url = "{}/nlp/pos".format(host_url)
        self.__sentiment_analysis_url = "{}/nlp/sentiment".format(host_url)
        self.__name_entity_recognition_url = "{}/nlp/ner".format(host_url)

    def response(self, request_id, return_type=None):
        """
        :type request_id: str
        :type return_type: type | None
        :rtype: bbridge_sdk.entity.response_wrapper.Response
        """
        response = requests.get(self.__response_url, params={"id": request_id}, headers=self.__headers)
        if response.status_code == 200:
            content = json.loads(response.text)
            if return_type is not None and issubclass(return_type, BBridgeEntity):
                content = return_type.from_json(content)
            return Response(response.status_code, content)
        elif response.status_code == 204:
            return Response(response.status_code)
        else:
            return Response(response.status_code, err_message=response.reason)

    def individual_user_profiling(self, user, lang, attr):
        """
        :type user: entity.user.User
        :type lang: str
        :type attr: list[str]
        :rtype: bbridge_sdk.entity.response_wrapper.Response
        """
        response = requests.post(self.__personal_profiling_url, params={"lang": lang, "attr": attr},
                                 headers=self.__headers, data=json.dumps(user, cls=BBridgeJSONEncoder))
        return BBridgeClient.__process_response(response)

    def image_objects_detection(self, object_detection_data):
        """
        :type object_detection_data: entity.object_detection_data.ObjectDetectionData
        :rtype: bbridge_sdk.entity.response_wrapper.Response
        """
        response = requests.post(self.__image_objects_url, headers=self.__headers,
                                 data=json.dumps(object_detection_data, cls=BBridgeJSONEncoder))
        return BBridgeClient.__process_response(response)

    def image_concepts_detection(self, concept_detection_data):
        """
        :type concept_detection_data: entity.concept_detection_data.ConceptDetectionData
        :rtype: bbridge_sdk.entity.response_wrapper.Response
        """
        response = requests.post(self.__image_concepts_url, headers=self.__headers,
                                 data=json.dumps(concept_detection_data, cls=BBridgeJSONEncoder))
        return BBridgeClient.__process_response(response)

    def pos_tagging(self, nlp_data, lang):
        """
        :type nlp_data: entity.nlp_data.NLPData
        :type lang: str
        :rtype: bbridge_sdk.entity.response_wrapper.Response
        """
        response = requests.post(self.__pos_tagging_url, params={"lang": lang},
                                 headers=self.__headers, data=json.dumps(nlp_data, cls=BBridgeJSONEncoder))
        return BBridgeClient.__process_response(response)

    def sentiment_analysis(self, nlp_data, lang):
        """
        :type nlp_data: entity.nlp_data.NLPData
        :type lang: str
        :rtype: bbridge_sdk.entity.response_wrapper.Response
        """
        response = requests.post(self.__sentiment_analysis_url, params={"lang": lang},
                                 headers=self.__headers, data=json.dumps(nlp_data, cls=BBridgeJSONEncoder))
        return BBridgeClient.__process_response(response)

    def name_entity_recognition(self, nlp_data, lang):
        """
        :type nlp_data: entity.nlp_data.NLPData
        :type lang: str
        :rtype: bbridge_sdk.entity.response_wrapper.Response
        """
        response = requests.post(self.__name_entity_recognition_url, params={"lang": lang},
                                 headers=self.__headers, data=json.dumps(nlp_data, cls=BBridgeJSONEncoder))
        return BBridgeClient.__process_response(response)

    class Builder:
        __headers = {"Content-type": "application/json"}

        def __init__(self, username, password, host_url=DEFAULT_HOST_URL):
            """
            :type username: str
            :type password: str
            :type host_url: str
            """
            self.__credential = json.dumps({"username": username, "password": password})
            self.__host_url = host_url
            self.__auth_url = "{}/auth".format(host_url)

        def build(self):
            """
            :rtype: BBridgeClient
            """
            response = requests.post(self.__auth_url, headers=self.__headers, data=self.__credential)
            token_object = json.loads(response.content)
            token = token_object["token"]

            return BBridgeClient(token, self.__host_url)

# -*- coding: utf-8 -*-
import json
import requests


class ThemeTagger(object):

    LEGACY_COOKIES = {
        'ASP.NET_SessionId': 'tbdoo1vctm5m0berpj1xtwue',
        '.ASPXAUTH': '58A8662D39B9834F893B9ED4A4359D815AF69CAF7962AB02A8040E0FBDA1AB61241C9'
                     'B513A0E7FB53A78715C1ACF3F1663EBF3E0487C2D9919563CDC4A3183F9BAE03A692B'
                     'C72A43EFE402F804E5FB034B6C48D343A8DC446942FF043B2190CA021C06A6C152CCD'
                     'ADEECB45E37859405AE32ECD20D7784E69F722D1541A0B2A9223E853A62F9DC008AB4'
                     'BB8E548372E375CF9BAC'
    }
    LEGACY_URL = 'https://app.youscan.io/'
    LEGACY_DELETE_TAG = 'Tag/DeleteTagFromTheme'

    URL = 'https://api.youscan.io/'
    API_PREFIX = 'api/themes/'
    SET_TAG = '/mentions/settags'
    LIST_TAG = '/tags'  # Get
    CREATE_TAG = '/tags'  # Post

    AUTH = {
        'Authorization': 'bearer AQAAANCMnd8BFdERjHoAwE_Cl-sBAAAANIU2osdu10Cy3scVCiP4tQAAAAACAAAAAAADZgAAwAAAABAAAAAiARAiy9dnyWgpaDSBz8FfAAAAAASAAACgAAAAEAAAAFjQVI1Qtod15wdE5n6zFE8AAQAAuU-uffn3YPc22XUR1UGVf58DZVRzl_zf5RDFnspKDE6h_dxuR_lSXUNj_sbIICi8t_VISEEwvfaIgmM5JtmVAmL0D-ZMuVDn8MyABZJz6IMRDLv_uAiUC83S4gGxXQC93ss15kUAzBA7-AhRn_RVBveGrwA5-s4pasznqBMQXCwNGs6jzSV5mOt3mqIlqFBrooSt2DxnnCihOlIyxh4eHIDcHbBCffyMA_W1u_gHgzGpsd-egdS772VjUHxF_Rf7hrmNKLz0n1grA-SYP8YtyoNMduIF4EaYFHf6gLEb2MuwxuhV80FRHFP3bp5Nw56P1uYDUAqoZx1sIMGf-PNHyRQAAAAftK4P9pPZ_87bGnBFIU0dinuDLw',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }

    AUTO_TAG_PREFIX = 'at'

    def __init__(self, theme_id, version, auth=None, legacy_auth=None):
        """
        Creates a tagger that utilizes YS new API and Legacy API (for tag deletion purpose).
        Automatically assigns prefix for tags: 'at-<version>:', which can be overriden
        via ThemeTagger.prefix field.
        For correct authorization a dict of {'Authorization': 'bearer <key>'}
        and {'ASP.NET_SesstionId': '<id>', '.ASPXAUTH': '<key>'} are to be provided
        for auth and legacy_auth respectively.
        """
        self.theme = theme_id
        self.version = version
        self.new_auth = auth
        self.new_legacy_auth = legacy_auth
        if self.new_auth:
            for key, value in self.new_auth.items():
                ThemeTagger.AUTH[key] = value
        if self.new_legacy_auth:
            for key, value in self.new_legacy_auth.items():
                ThemeTagger.LEGACY_COOKIES[key] = value
        self.prefix = ThemeTagger.AUTO_TAG_PREFIX + '-' + str(version) + ':'

    def delete_auto_tags(self):
        active_tags = self.list_tags()
        return self.delete_tags(self.__find_auto_tags(active_tags))

    def __find_auto_tags(self, id_tag_map):
        return {k: v for k, v in id_tag_map.items() if self.__is_auto_tag_name(v)}

    def __to_auto_tag_names(self, tag_names):
        return {self.__auto_tag_name(name) for name in tag_names}

    def __auto_tag_name(self, name):
        return self.prefix + name

    def __is_auto_tag_name(self, name):
        return name.startswith(self.prefix)

    def delete_tag(self, id_and_tag):
        url = ThemeTagger.LEGACY_URL + ThemeTagger.LEGACY_DELETE_TAG
        query = {
            'themeId': str(self.theme),
            'tag': id_and_tag[1]
        }
        request_result = requests.post(url=url, json=query, cookies=ThemeTagger.LEGACY_COOKIES)
        if 'success' in request_result.json() and request_result.json()['success']:
            print('[DELETE TAG] ' + repr(query))
            return id_and_tag[0]
        else:
            print('[DELETE TAG] FAILED: ' + repr(query) + repr(json.dumps(request_result.json(), ensure_ascii=False, indent=2)))
            return None

    def delete_tags(self, id_tag_map):
        deleted = dict()
        for tag_id in id_tag_map:
            id_ = self.delete_tag((tag_id, id_tag_map[tag_id]))
            if id_:
                deleted[id_] = id_tag_map[id_]
        return deleted

    def create_tag(self, tag_name):
        url = ThemeTagger.URL + ThemeTagger.API_PREFIX + str(self.theme) + ThemeTagger.LIST_TAG

        query = {
            'name': tag_name
        }
        request_result = requests.post(url=url, json=query, headers=ThemeTagger.AUTH)
        result_json = request_result.json()
        if 'id' in result_json:
            print('[CREATE TAG] ' + repr(json.dumps(result_json, ensure_ascii=False, indent=2)))
            return result_json['id']
        else:
            print('[CREATE TAG] FAILED: ' + repr(query) + ' with: ' + repr(json.dumps(result_json, ensure_ascii=False, indent=2)))
            return None

    def create_tags(self, tag_names):
        created_tags = dict()
        for tag_name in tag_names:
            id_ = self.create_tag(tag_name)
            if id_:
                created_tags[id_] = tag_name
        return created_tags

    def list_tags(self):
        url = ThemeTagger.URL + ThemeTagger.API_PREFIX + str(self.theme) + ThemeTagger.LIST_TAG

        request_result = requests.get(url=url, headers=ThemeTagger.AUTH)
        print('[LIST TAGS] ' + repr(json.dumps(request_result.json(), ensure_ascii=False, indent=2)))
        return {entry['id']: entry['name'] for entry in request_result.json()['tags']}

    def set_tags(self, ids, tag_ids):
        query = {
            'ids': ids,
            'filter': {'from': '2010-01-01', 'to': '2017-12-31'},
            'add': tag_ids
        }
        url = ThemeTagger.URL + ThemeTagger.API_PREFIX + str(self.theme) + ThemeTagger.SET_TAG
        request_result = requests.put(url=url, json=query, headers=ThemeTagger.AUTH)
        print('[SET TAGS] ' + repr(json.dumps(request_result.json(), ensure_ascii=False, indent=2)))
        return request_result.json()['processId']\
            if 'lrt' not in request_result.json() or not request_result.json()['lrt']\
            else None

    def apply_auto_tagging(self, ids, tag, batch_size=500):
        import math
        batch = batch_size
        auto_tag = self.__auto_tag_name(tag)
        tag_id = self.create_tag(auto_tag)
        for i in range(0, math.ceil(len(ids) / batch)):
            start = i * batch
            end = start + batch
            self.set_tags(ids[start:end], [tag_id])

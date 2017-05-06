# coding: UTF-8

import requests, json


class SendCloud(object):
    """使用 sendcloud.sohu.com MDS"""

    template_send_url = "http://sendcloud.sohu.com/webapi/mail.send_template.json"

    def __init__(self, api_user, api_key, from_addr, fromname=None, replyto=None):
        self.api_user = api_user
        self.api_key = api_key

        self.from_addr = from_addr
        self.fromname = fromname
        self.replyto = replyto

    def template_send(self, template_name, subject, sub_vars):
        """通过预先配置的模板发送邮件"""

        params = {
            "api_user": self.api_user,
            "api_key": self.api_key,
            "from": self.from_addr,
            "template_invoke_name": template_name,
            "substitution_vars": json.dumps(sub_vars),
            "subject": subject,
            "resp_email_id": "true",
        }
        if self.fromname:
            params["fromname"] = self.fromname
        if self.replyto:
            params["replyto"] = self.replyto

        r = requests.post(self.template_send_url, data=params)
        # TODO: fix me!
        print(r.text)
        return r.json()

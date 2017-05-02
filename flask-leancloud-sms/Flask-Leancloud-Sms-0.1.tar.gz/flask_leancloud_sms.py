# -*- coding: utf-8 -*-
import json
import requests
class Leancloud_Sms(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    def init_app(self,app):
        self._app_id = app.config.get('LEANCLOUD_APP_ID', '')
        self._app_key = app.config.get('LEANCLOUD_APP_KEY', '')
        self._request_sms_code_url = app.config.get('REQUEST_SMS_CODE_URL', 'https://api.leancloud.cn/1.1/requestSmsCode')
        self._verify_sms_code_url = app.config.get('VERIFY_SMS_CODE_URL', 'https://api.leancloud.cn/1.1/verifySmsCode/')
        
        self._headers = {
            "X-LC-Id": self._app_id,
            "X-LC-Key": self._app_key,
            "Content-Type": "application/json",
        }
    def send_message(self,phone,smsType='sms',countryCode='CN',template=None,**argv):
        """
        通过 POST 请求 requestSmsCode API 发送验证码到指定手机
        :param phone: 电话号
        :param smsType: 验证类型
        :param countryCode: 国家类型
        :param template: 短信模板
        :param argv: 模板参数
        :return: bool值
        """
        data = {
            "mobilePhoneNumber": phone,
            "smsType":smsType,
            "countryCode":countryCode,
        }
        if template is not None:
            data['template']=template,
            data=dict(data,argv)
        
        # post 方法参数包含三部分，如我们之前分析 API 所述
        # REQUEST_SMS_CODE_URL: 请求的 URL
        # data: 请求的内容，另外要将内容编码成 JSON 格式
        # headers: 请求的头部，包含 Id 与 Key 等信息
        r = requests.post(self._request_sms_code_url, data=json.dumps(data), headers=self._headers)
        # 响应 r 的 status_code 值为 200 说明响应成功
        # 否则失败
        if r.status_code == 200:
            return True
        else:
            return False
    def verify_sms(self,phone, code):
        """
        发送 POST 请求到 verifySmsCode API 获取校验结果
        :param phone: 电话号
        :param code: 验证码
        :return: 
        """
        # 使用传进的参数 code 与 phone 拼接出完整的 URL
        target_url = self._verify_sms_code_url + "%s?mobilePhoneNumber=%s" % (code, phone)

        r = requests.post(target_url, headers=self._headers)
        # 响应 r 的 status_code 值为 200 说明验证成功
        # 否则失败
        if r.status_code == 200:
            return True
        else:
            return False
        
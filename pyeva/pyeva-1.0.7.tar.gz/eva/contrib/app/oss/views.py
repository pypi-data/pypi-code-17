# coding: utf-8

import datetime
import logging

from eva.web import APIRequestHandler, authenticated
from eva.utils.translation import ugettext_lazy as _

from .utils import save_single_file


class SimditorImageUpload(APIRequestHandler):
    '''Simditor 图片上传 API

    # simditor 需要的格式
    {
        "success": true/false,
        "msg": "error message", # optional
        "file_path": "[real file path]"
    }
    '''

    @authenticated
    def post(self):
        print(self.request)
        if self.request.files and 'fileDataFileName' in self.request.files:
            filedata = self.request.files['fileDataFileName']
            attachment, emsg = save_single_file(self.db, filedata, self.current_user)

            if attachment:
                d = {
                    "success": True,
                    "file_path": attachment.static_url,
                }
            else:
                d = {
                    "success": False,
                    "msg": emsg,
                }

        else:
            d = {
                "success": False,
                "msg": _("No files to upload!"),
            }

        # TODO: fix me!
        self.success(data=d)

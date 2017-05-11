#coding: utf8

from django.db import models
from .widgets import QiniuWidget

class QiniuField(models.CharField):

    def __init__(self,qiniu_field,btn_title=u'上传文件',*args,**kwargs):
        self.qiniu_field = qiniu_field
        self.btn_title = btn_title
        super(QiniuField,self).__init__(*args,**kwargs)


    def deconstruct(self):
        name, path, args, kwargs = super(QiniuField, self).deconstruct()
        kwargs['qiniu_field'] = self.qiniu_field
        kwargs['btn_title'] = self.btn_title
        return name,path,args,kwargs


    def formfield(self, **kwargs):
        kwargs['widget'] = QiniuWidget(btn_title=self.btn_title,qiniu_field=self.qiniu_field)
        return super(QiniuField,self).formfield(**kwargs)

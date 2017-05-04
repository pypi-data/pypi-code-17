from django.conf.urls import *
from django.conf import settings

from cl_utils.inline_edit.views import *

urlpatterns = patterns('',
    url(r'^inline-edit/save/$', inline_edit_callback, name='inline_edit_save'),
)

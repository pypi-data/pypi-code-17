
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings

import os
import shutil
from datetime import datetime


########################################################################
class ZipThis(View):
    """"""

    #----------------------------------------------------------------------
    def get(self, request):
        """"""
        filename = os.path.join(os.path.dirname(settings.BASE_DIR), 'django_project_{}'.format(datetime.now()))
        shutil.make_archive(filename, 'zip', settings.BASE_DIR)
        response = HttpResponse(open('{}.zip'.format(filename), 'rb'), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="project.zip"'

        return response



########################################################################
class Settings(View):
    """"""

    #----------------------------------------------------------------------
    def get(self, request):
        """"""
        settings.ANDROID.update({'SETTINGS_MODULE': settings.SETTINGS_MODULE})
        return JsonResponse(settings.ANDROID)


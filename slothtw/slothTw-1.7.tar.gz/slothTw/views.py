from django.shortcuts import render
from django.http import JsonResponse, Http404
from djangoApiDec.djangoApiDec import queryString_required, date_proc, queryString_required_ClassVersion
from django.core import serializers
from django.forms.models import model_to_dict
from slothTw.models import *
from django.views import View
import json

# Create your views here.
@queryString_required(['school', 'start'])
def clist(request):
    start = int(request.GET['start']) -1 
    result = Course.objects.filter(school=request.GET['school'])[start:start+15]
    return JsonResponse(json.loads(serializers.serialize('json', list(result), fields=('name', 'avatar', 'teacher'))), safe=False)

@queryString_required(['id'])
def cvalue(request):
    try:
        result = model_to_dict(Course.objects.get(id=request.GET['id']))
        result['avatar'] = result['avatar'].url if result['avatar'] else None
        return JsonResponse(result, safe=False)
    except Exception as e:
        raise

@queryString_required(['school', 'name', 'teacher'])
def search(request):
    try:
        result = model_to_dict(Course.objects.get(school=request.GET['school'], name=request.GET['name'],teacher=request.GET['teacher']))
        result['avatar'] = result['avatar'].url if result['avatar'] else None
        return JsonResponse([result], safe=False)
    except Exception as e:
        nameList = Course.objects.filter(school=request.GET['school'], name__contains=request.GET['name'])
        teacherList = Course.objects.filter(school=request.GET['school'], teacher__contains=request.GET['teacher'])
        return JsonResponse(json.loads(serializers.serialize('json', list(nameList) + list(teacherList))), safe=False)


# 顯示特定一門課程的留言評論
@queryString_required(['id', 'start'])
def comment(request):
    try:
        start = int(request.GET['start']) - 1
        c = Course.objects.get(id=request.GET['id'])
        result = c.comment_set.all()[start:start+15]
        return JsonResponse(json.loads(serializers.serialize('json', list(result))), safe=False)
    except Exception as e:
        raise
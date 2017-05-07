from django.shortcuts import render
from django.http import JsonResponse, Http404
from djangoApiDec.djangoApiDec import queryString_required, date_proc, queryString_required_ClassVersion
from django.core import serializers
from django.forms.models import model_to_dict
from slothTw.models import *
from django.views import View
from django.db.models import F
import json

# Create your views here.
@queryString_required(['school', 'start'])
def clist(request):
    start = int(request.GET['start']) -1
    ctype = request.GET['ctype'] if 'ctype' in request.GET else '通識'

    querySet = Course.objects.filter(school=request.GET['school'], ctype=ctype)
    length = len(querySet) // 15
    querySet = querySet[start:start+15]
    result = json.loads(serializers.serialize('json', list(querySet[start:start+15]), fields=('name', 'ctype', 'avatar', 'teacher', 'school', 'feedback_amount')))
    for index, i in enumerate(querySet):
        result[index]['fields']['avatar'] = i.avatar.url
    return JsonResponse([{'TotalPage':length, 'school':request.GET['school'], 'ctype':ctype}] + result, safe=False)

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
        nameList = Course.objects.filter(school=request.GET['school'], name__contains=request.GET['name'])[:5]
        teacherList = Course.objects.filter(school=request.GET['school'], teacher__contains=request.GET['teacher'])[:5]
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

@queryString_required(['id'])
def like(request):
    request.GET = request.GET.copy()
    request.GET['start'] = 15
    if request.POST:
        if request.POST.dict()['like'] == '1':
            Comment.objects.filter(id=request.GET['id']).update(like=F('like') + 1)
            return comment(request)

@queryString_required(['id'])
def questionnaire(request):
    id = request.GET['id']
    c = Course.objects.get(id=id)
    if request.method == 'POST' and request.POST:
        if 'rating' in request.POST:
            data = json.loads(request.POST.dict()['rating'])
            amount = c.feedback_amount + 1
            modelDict = {'feedback_amount':amount}
            modelDict['feedback_freedom'] = (c.feedback_freedom*(amount-1) + (data[0]*3/4 + data[1]/4)) /amount
            modelDict['feedback_GPA'] = (c.feedback_GPA*(amount-1) + data[2]) / amount
            modelDict['feedback_easy'] = (c.feedback_easy*(amount-1) + (data[3]/12 + data[4]/12  + data[7]*9/12 + data[8]/12)) / amount
            modelDict['feedback_knowledgeable'] = (c.feedback_knowledgeable*(amount-1) + data[6]) / amount
            modelDict['feedback_FU'] = (c.feedback_FU*(amount-1) + data[5]) / amount
            Course.objects.update_or_create(id=id, defaults=modelDict)
            return cvalue(request)

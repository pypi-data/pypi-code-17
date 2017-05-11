from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from ohm2_handlers_light.parsers import get_as_or_get_default
from . import dispatcher



@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
	keys = (
		("username", "username", ""),
		("email", "email", ""),
		("password", "password", ""),
	)
	ret, error = dispatcher.signup(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error" : "an error occured"})
	return JsonResponse(ret)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
	keys = (
		("username", "username", ""),
		("password", "password", ""),
	)
	ret, error = dispatcher.login(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error" : "an error occured"})
	return JsonResponse(ret)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def logout(request):
	keys = (
	)
	ret, error = dispatcher.logout(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error" : "an error occured"})
	return JsonResponse(ret)		
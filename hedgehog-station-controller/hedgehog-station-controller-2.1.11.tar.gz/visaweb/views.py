from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets, views, serializers, response, status, decorators
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from django.contrib.auth.models import User, Group
from .models import Asset

import logging
import assetadapter

from .serializers import UserSerializer, GroupSerializer, AssetSerializer,AssetListSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)

def synchronize():
    asset_list = Asset.objects.all()
    mapping = {}
    for a in asset_list:
        mapping[a.alias] = a.address
    assetadapter.dm.alias(mapping)

synchronize()

# Create your views here.
def health(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    asset_list = Asset.objects.all()
    context = {
        'shell': 'visaweb/src/hedgehog-app.html',
        'shell_element': 'hedgehog-app',
        'asset_list': asset_list
    }
    return render(request, 'visaweb/index.html', context)

def detail(request, asset_id):
    return HttpResponse("You're looking at question %s." % asset_id)

def results(request, asset_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % asset_id)

def vote(request, asset_id):
    return HttpResponse("You're voting on question %s." % asset_id)

@permission_classes((permissions.AllowAny,))
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@permission_classes((permissions.AllowAny,))
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes((permissions.AllowAny,))
class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

@decorators.api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def visa_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            data = assetadapter.dm.list()
            return response.Response(data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

@decorators.api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def devicemanager_active(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            resources = assetadapter.dm.list()
            connected_assets = Asset.objects.filter(address__in=resources)
            return response.Response(AssetSerializer(connected_assets, many=True).data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

@decorators.api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def devicemanager_inactive(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            resources = assetadapter.dm.list()
            connected_assets = Asset.objects.exclude(address__in=resources).all()
            logging.info('-------------- Inactive assets:', connected_assets)
            return response.Response(AssetSerializer(connected_assets, many=True).data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

@decorators.api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def devicemanager_unknown(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            resources = assetadapter.dm.list()
            asset_addresses = Asset.objects.all().values_list('address')

            result = [item for item in resources if item not in asset_addresses]

            return response.Response(result, status=status.HTTP_201_CREATED)
        except Exception as error:
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

@decorators.api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def visa_alias(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        try:
            connected = assetadapter.dm.alias(request.data)
            return response.Response(status=status.HTTP_200_OK)
        except Exception as error:
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

@decorators.api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def devicemanager_attach(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        try:
            mapping = {}

            alias = request.data['key']
            if (alias == None):
                alias = 'asset' + str(Asset.objects.count())

            address = request.data['value']

            mapping[alias] = address

            connected = assetadapter.dm.alias(mapping)

            if (connected == 1):
                a = Asset(alias=alias, address=address)
                a.save()
                return response.Response({ u'id': a.id }, status=status.HTTP_200_OK)
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

@decorators.api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def visa_read(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        try:
            logger.info('Execute VISA command: read')
            data = assetadapter.dm.read(request.data['alias'], request.data['command'])
            return response.Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return response.Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@decorators.api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def visa_write(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        try:
            logger.info('Execute VISA command: write')
            data = assetadapter.dm.write(request.data['alias'], request.data['command'])
            return response.Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return response.Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@decorators.api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def visa_query(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        try:
            logger.info('Execute VISA command: query')
            data = assetadapter.dm.query(request.data['alias'], request.data['command'])
            return response.Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return response.Response({ 'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
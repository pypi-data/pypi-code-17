# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from rest_framework import permissions, status
from rest_framework.decorators import detail_route, api_view, permission_classes
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.routers import APIRootView
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from assetadapter.models import Asset, Property, ChoiceProperty, EnumerationChoice, EnumerationType
from assetadapter.serializers import AssetSerializer, PropertySerializer, PropertyUnitChoiceListSerializer
from assetadapter.tasks import list_resources


class AssetListView(ListView):
    model = Asset
    template_name = 'assetadapter/index.html'

    def get_queryset(self):
        """Return the last five published questions."""
        return Asset.objects.order_by('-alias')[:10]


class AssetDetailView(DetailView):
    model = Asset
    template_name = 'assetadapter/detail.html'


class AssetConsoleView(DetailView):
    model = Asset
    template_name = 'assetadapter/console.html'


class AssetViewSet(ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class PropertyViewSet(ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    permission_classes = (permissions.AllowAny,)

    @detail_route(renderer_classes=[StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        property = self.get_object()
        return Response(property.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# @api_view(['GET'])
# @csrf_exempt
# @permission_classes((permissions.AllowAny,))
class ActiveDeviceListView(ReadOnlyModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def get(self, request, format=None):
        """
        List all snippets, or create a new snippet.
        """

        if request.method == 'GET':
            try:
                r = list_resources.delay()
                resources = r.get(timeout=1)
                if resources == None:
                    resources = []
                connected_assets = Asset.objects.filter(address__in=resources)
                return Response(AssetSerializer(connected_assets, many=True).data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @csrf_exempt
# @permission_classes((permissions.AllowAny,))
class InactiveDeviceListView(ReadOnlyModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def get(self, request, format=None):
        """
        List all snippets, or create a new snippet.
        """
        if request.method == 'GET':
            try:
                r = list_resources.delay()
                resources = r.get(timeout=1)
                if resources == None:
                    resources = []
                disconnected_assets = Asset.objects.exclude(address__in=resources).all()
                return Response(AssetSerializer(disconnected_assets, many=True).data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @csrf_exempt
# @permission_classes((permissions.AllowAny,))
class UnknownDeviceListView(ReadOnlyModelViewSet):
    r = list_resources.delay()
    queryset = r.get(timeout=1)
    model = str

    def get(self, request, format=None):
        """
        List all snippets, or create a new snippet.
        """

        if request.method == 'GET':
            try:
                r = list_resources.delay()
                resources = r.get(timeout=1)
                if resources == None:
                    resources = []
                asset_addresses = Asset.objects.all().values_list('address')

                result = [item for item in resources if item not in asset_addresses]

                return Response(result, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@permission_classes((permissions.AllowAny,))
@api_view(['GET'])
def list_unit_choices(request, pk):
    """
    List all snippets, or create a new snippet.
    """

    if request.method == 'GET':
        try:
            cp = EnumerationType.objects.get(property=pk)
            results = EnumerationChoice.objects.filter(owner_id=cp.pk).all()
            serializer = PropertyUnitChoiceListSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': error.message, 'exception': '{}'.format(type(error).__name__, error.args)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@permission_classes((permissions.AllowAny,))
@api_view(['GET'])
def list_property_value_choices(request, pk):
    """
    List all snippets, or create a new snippet.
    """

    if request.method == 'GET':
        try:
            cp = EnumerationType.objects.get(enumerationchoice=pk)
            results = EnumerationChoice.objects.filter(owner_id=cp.pk).all()
            serializer = PropertyUnitChoiceListSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': error.message, 'exception': '{}'.format(type(error).__name__, error.args)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
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
                asset_count = Asset.objects.count()
                alias = 'asset' + str(asset_count)

            address = request.data['value']

            mapping[alias] = address

            connected = alias.delay(mapping).get(timeout=1)['connected']

            if (connected > 0):
                a = Asset(alias=alias, address=address)
                a.save()
                return Response({u'id': a.id}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

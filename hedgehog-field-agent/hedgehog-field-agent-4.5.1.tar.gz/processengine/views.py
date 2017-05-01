# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from django.db.models.functions import datetime
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_celery_results.models import TaskResult
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from processengine.models import Process, Execution, DONE, FAILURE, DISABLED, PENDING, INITIALIZED, RUNNING
from processengine.serializers import ProcessSerializer, ExecutionSerializer, TaskResultSerializer

logger = logging.getLogger(__name__)

class TaskResultViewSet(ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer

    @list_route(methods=['get'])
    def get_queryset(self):
        execution_id = self.kwargs['execution']
        logger.warning("Get results of execution %s" % execution_id)
        return Execution.objects.get(pk=execution_id).result

class AllProcessViewSet(ReadOnlyModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer

class AllExecutionViewSet(ReadOnlyModelViewSet):
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer

class HictoricalExecutionViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ExecutionSerializer
    queryset = Execution.objects.filter(status__in=[PENDING, DISABLED, FAILURE, DONE, INITIALIZED])
    """
    List all snippets, or create a new snippet.
    """

    @list_route(methods=['get'])
    def get_queryset(self):
        process_id = self.kwargs['process']
        logger.warning("Get execution from process %s" % process_id)
        return Execution.objects.filter(
            # ended__lte=datetime.datetime.now(),
            executor=process_id,
            status__in=[PENDING, DISABLED, FAILURE, DONE, INITIALIZED]
        )


class RunningExecutionViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ExecutionSerializer
    queryset = Execution.objects.filter(status__in=[RUNNING])
    """
    List all snippets, or create a new snippet.
    """

    @list_route(methods=['get'])
    def get_queryset(self):
        process_id = self.kwargs['process']
        logger.warning("Get execution from process %s" % process_id)
        return Execution.objects.filter(
            # ended__lte=datetime.datetime.now(),
            executor=process_id,
            status__in=[RUNNING]
        )


        # def get_completed_executions(self, request, slug, format=None):
        #     logger.info("Get execution from process %s" % slug)
        #
        #     executions = Execution.objects.filter(
        #         # ended__lte=datetime.datetime.now(),
        #         executor=slug,
        #         status__in=[PENDING, DISABLED, FAILURE, DONE, INITIALIZED])
        #
        #     # page = self.paginate_queryset(executions)
        #     # if page is not None:
        #     #     serializer = self.get_serializer(page, many=True)
        #     #     return self.get_paginated_response(serializer.data)
        #     serializer = self.get_serializer(executions, many=True)
        #     return Response(serializer.data)


@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def run_process_definition(request, pk):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        try:

            processDefinition = Process.objects.get(pk=pk)
            # signal = request.data['signal']
            processDefinition.run()
            serializer = ProcessSerializer(processDefinition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RunningProcessViewSet(ReadOnlyModelViewSet):
    pass


class HystoricalProcessViewSet(ReadOnlyModelViewSet):
    pass

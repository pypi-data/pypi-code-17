# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging
from formtools.wizard.views import SessionWizardView
from django.db.models.functions import datetime
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_celery_results.models import TaskResult
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from viewflow.decorators import flow_start_view, flow_view
from viewflow.flow.views import StartFlowMixin, get_next_task_url

import processengine
from assetadapter.models import Property
from assetadapter.serializers import PropertySerializer
from processengine import forms
from processengine.models import Execution, DONE, FAILURE, DISABLED, PENDING, INITIALIZED, RUNNING, Process
from processengine.serializers import ProcessSerializer, ExecutionSerializer, TaskResultSerializer, \
    ParameterPropertySerializer

from processengine.tasks import execute_process

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TaskDashboardView(StartFlowMixin, SessionWizardView):
    template_name = 'processengine/parameters.html'

    form_list = [forms.TaskSubjectForm, forms.TaskParametersForm]

    def done(self, form_list, form_dict, **kwargs):
        asset = form_dict['0'].save()

        parameters = form_dict['1'].save(commit=False)
        parameters.save()

        self.activation.process.sample = parameters
        self.activation.done()

        return redirect(get_next_task_url(self.request, self.activation.process))



@flow_start_view
def additional_parameter_set(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.AssetForm(request.POST or None)

    if form.is_valid():
        parameters = form.save(commit=False)

        # sample.alias = form.cleaned_data['alias']
#         sample.address = form.cleaned_data['address']
#         sample.taken_by = request.user
        parameters.save()
#
        request.activation.process.parameters = parameters
        request.activation.done()
#
        return redirect(get_next_task_url(request, request.activation.process))
#
    return render(request, 'processengine/predefined-parameters.html', {
        'form': form,
        'activation': request.activation
    })

#
@flow_view
def task_data(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.TaskOutputForm(request.POST or None)

    if form.is_valid():
        data_volume = form.save(commit=False)
        data_volume.sample = request.activation.process.sample
        data_volume.save()
        request.activation.done()
        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'bloodtest/bloodtest/task-results.html', {
        'form': form,
        'activation': request.activation
    })



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

class AllPropertyViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ParameterPropertySerializer
    queryset = Property.objects.all()

class InputPropertyViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    """
    List all snippets, or create a new snippet.
    """

    @list_route(methods=['get'])
    def get_queryset(self):
        process_id = self.kwargs['process']
        logger.warning("Get input properties of process %s" % process_id)
        return processengine.models.Process.objects.get(pk=process_id).input_parameters

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
            # processDefinition.run(variables=processDefinition.parameters)

            execute_process.delay(processDefinition.id, processDefinition.parameters)



            serializer = ProcessSerializer(processDefinition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def save_default_parameters(request, pk):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        try:
            process = Process.objects.get(pk=pk)
            for key, value in request.data.items():
                try:
                    p = Property.objects.get(name=key)
                    process.input_parameters.add(p)
                    if value is None:
                        request.data[key] = p.get_default_value()
                except Exception as ex:
                    logger.error('Parameter %s could not set to %s' % (key, value))
            process.parameters = json.dumps(request.data)
            process.save()
            # signal = request.data['signal']
            serializer = ProcessSerializer(process)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RunningProcessViewSet(ReadOnlyModelViewSet):
    pass


class HystoricalProcessViewSet(ReadOnlyModelViewSet):
    pass

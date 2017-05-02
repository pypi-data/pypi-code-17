from django_celery_results.models import TaskResult
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

import processengine
from assetadapter.models import Property
from assetadapter.serializers import PropertySerializer, AssetSerializer
from processengine.models import Execution


class TaskResultSerializer(serializers.Serializer):

    class Meta:
        model = TaskResult
        fields = ('task_id', 'status', 'result', 'date_done', 'traceback', 'meta')

class ExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execution
        fields = ('id', 'begins', 'result', 'status')

class ParameterPropertySerializer(PropertySerializer):
    owner = AssetSerializer(read_only=True)

    class Meta:
        model = Property
        fields = (
        'id', 'name', 'display_name', 'description', 'type', 'getter_command', 'setter_command', 'unit_choices',
        'default_unit', 'owner')


class ProcessSerializer(serializers.ModelSerializer):
    executions = ExecutionSerializer(many=True, read_only=True)
    input_parameters = PropertySerializer(many=True, read_only=True)
    output_parameters = PropertySerializer(many=True, read_only=True)
    last_execution = ExecutionSerializer(many=False, read_only=True)
    # owner = PrimaryKeyRelatedField(queryset=Process.objects.all())

    class Meta:
        model = processengine.models.Process
        fields = ('id', 'name', 'display_name', 'description', 'status', 'executions', 'output_parameters', 'input_parameters', 'last_execution')
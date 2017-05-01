from django_celery_results.models import TaskResult
from rest_framework import serializers

from processengine.models import Process, Execution


class TaskResultSerializer(serializers.Serializer):

    class Meta:
        model = TaskResult
        fields = ('task_id', 'status', 'result', 'date_done', 'traceback', 'meta')

class ExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execution
        fields = ('id', 'begins', 'result', 'status')

class ProcessSerializer(serializers.ModelSerializer):
    executions = ExecutionSerializer(many=True, read_only=True)

    class Meta:
        model = Process
        fields = ('id', 'name', 'display_name', 'description', 'status', 'executions')
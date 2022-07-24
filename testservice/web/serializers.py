from os.path import exists

from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from web.models import Task

TASK_READ_ONLY_FIELDS = (
    'created_at',
    'started_at',
    'finished_at',
    'status',
    'result',
    'status'
)


class TaskSerializer(ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()

    def validate_csv_file_name(self, value):
        if not exists(f'{settings.CSV_FILES_FOLDER}/{value}'):
            raise serializers.ValidationError(f'File {value} doesn\'t exist')
        return value

    class Meta:
        model = Task
        fields = (
            'csv_file_name',
            *TASK_READ_ONLY_FIELDS
        )
        extra_kwargs = {
            field: {'read_only': True} for field in TASK_READ_ONLY_FIELDS
        }

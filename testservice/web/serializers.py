from os.path import exists

from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from web.tasks import parse_csv_file

from web.models import Task

TASK_READ_ONLY_FIELDS = (
    'id',
    'created_at',
    'started_at',
    'finished_at',
    'status',
    'result',
)


class TaskSerializer(ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            *TASK_READ_ONLY_FIELDS,
            'csv_file_name',
        )
        read_only_fields = TASK_READ_ONLY_FIELDS

    def get_status(self, obj):
        return obj.get_status_display()

    def validate_csv_file_name(self, value):
        if not exists(f'{settings.CSV_FILES_FOLDER}{value}'):
            raise serializers.ValidationError(f'File {value} doesn\'t exist')
        return value

    def create(self, validated_data):
        instance = super().create(validated_data)
        parse_csv_file.delay(instance.id)
        return instance

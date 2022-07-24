from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from web.models import Task
from web.serializers import TaskSerializer
from web.tasks import parse_csv_file


class TaskApiView(ModelViewSet):
    queryset = Task.objects.filter()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Task.objects.filter(status=Task.IN_PROGRESS)
        return super(TaskApiView, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        parse_csv_file.delay(serializer.instance.id)
        headers = self.get_success_headers(serializer.data)
        return Response({'id': serializer.instance.id}, status=status.HTTP_201_CREATED, headers=headers)

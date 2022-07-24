from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from web.models import Task
from web.serializers import TaskSerializer


class TaskApiView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Task.objects.filter()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(status=Task.IN_PROGRESS)
        return super().list(request, *args, **kwargs)

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from web.views import TaskApiView

router = DefaultRouter()
router.register('tasks', TaskApiView, basename='tasks')

urlpatterns = [
    path('', include(router.urls))
]

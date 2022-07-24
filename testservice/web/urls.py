from django.urls import path

from web.views import TaskApiView

urlpatterns = [
    path('tasks/', TaskApiView.as_view({'get': 'list', 'post': 'create'}), name='task-list-create'),
    path('tasks/<int:pk>/', TaskApiView.as_view({'get': 'retrieve'}), name='task-retrieve'),
]

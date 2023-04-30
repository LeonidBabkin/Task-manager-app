from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.TasksView.as_view(), name='tasks'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    # path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    # path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
]

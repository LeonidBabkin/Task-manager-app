from django.urls import path
from task_manager.labels import views


urlpatterns = [
    path('', views.LabelsView.as_view(), name='labels'),
    path('create/', views.LabelCreateView.as_view(), name='label_create'),
    # path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    # path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    # path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]

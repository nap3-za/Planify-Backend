from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name="event"


urlpatterns = [
]


event_router = DefaultRouter()
event_router.register("events", views.EventViewSet, basename="event")
urlpatterns += event_router.urls

task_router = DefaultRouter()
task_router.register("tasks", views.TaskViewSet, basename="task")
urlpatterns += task_router.urls
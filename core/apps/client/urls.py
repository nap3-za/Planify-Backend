from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name="client"


urlpatterns = [
]


client_router = DefaultRouter()
client_router.register("client", views.ClientViewSet, basename="client")
urlpatterns += client_router.urls
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name="client"


urlpatterns = [
	path("clients/dashboard-data/", views.DashboardView.as_view(), name="dashboard-data"),
]


client_router = DefaultRouter()
client_router.register("", views.ClientViewSet, basename="client")
urlpatterns += client_router.urls
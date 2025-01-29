from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name="misc"


urlpatterns = [
	path("dashboard-data/", views.DashboardView.as_view(), name="dashboard-data"),
]

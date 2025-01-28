from rest_framework import (
	generics,
	status,
	pagination,
	mixins,
	viewsets,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
	EventSerializer,
	TaskSerializer,
)
from .models import (
	Event,
	Task,
)


class EventViewSetPagination(pagination.PageNumberPagination):
	page_size = 5
	page_size_query_param = "size"
	max_page_size = 5

class EventViewSet(viewsets.ModelViewSet):

	queryset = Event.objects.all()
	serializer_class = EventSerializer
	pagination_class = EventViewSetPagination


class TaskViewSetPagination(pagination.PageNumberPagination):
	page_size = 5
	page_size_query_param = "size"
	max_page_size = 5

class TaskViewSet(viewsets.ModelViewSet):

	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	pagination_class = TaskViewSetPagination


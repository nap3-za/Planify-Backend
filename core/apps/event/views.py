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


	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		queryset = queryset.filter(coordinator=request.user)

		#  - - -
		serializer = None
		paginate = True

		if request.GET and request.data:
			q = request.data

			if q["filters"]:
				queryset = queryset.filter(**q["filters"])

			elif q["single"]:
				queryset = queryset.objects.get(**q["single"])
				paginate = False

		if paginate:
			page = self.paginate_queryset(queryset)
			if page is not None:
				serializer = self.get_serializer(page, many=True)
				return self.get_paginated_response(serializer.data)
			serializer = self.get_serializer(queryset, many=True)
		else:
			serializer = self.get_serializer(queryset, context=self.get_serializer_context())


		return Response(serializer.data)



class TaskViewSetPagination(pagination.PageNumberPagination):
	page_size = 5
	page_size_query_param = "size"
	max_page_size = 5

class TaskViewSet(viewsets.ModelViewSet):

	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	pagination_class = TaskViewSetPagination


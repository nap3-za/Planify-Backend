from datetime import datetime,timedelta

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

	EventSummarySerializer,
	TaskSummarySerializer,
)
from .models import (
	Event,
	Task,
)



class EventViewSetPagination(pagination.PageNumberPagination):
	page_size = 25
	page_size_query_param = "size"
	max_page_size = 25

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

		if request.GET:
			q = request.GET.dict()

			if "filter" in q:
				del q["filter"]
				queryset = queryset.filter(**q)

			elif "single" in q:
				del q["single"]
				queryset = queryset.filter(**q)[0]
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


	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		queryset = queryset.filter(event__coordinator=request.user)

		#  - - -
		serializer = self.serializer_class
		paginate = True

		if request.GET:
			q = request.GET.dict()

			if "summary" in q:
				del q["summary"]
				serializer = TaskSummarySerializer

			if "filter" in q:
				del q["filter"]
				queryset = queryset.filter(**q)

			elif "single" in q:
				del q["single"]
				queryset = queryset.filter(**q)[0]
				paginate = False

		if paginate:
			page = self.paginate_queryset(queryset)
			if page is not None:
				serializer = serializer(page, many=True)
				return self.get_paginated_response(serializer.data)
			serializer = serializer(queryset, many=True)
		else:
			serializer = serializer(queryset)


		return Response(serializer.data)


class DashboardView(generics.GenericAPIView):

	def get(self, request, *args, **kwargs):
		queryset = Event.objects.filter(coordinator=request.user)
		response_data = {
			"stats": None,
			"events": None,
		}

		# Set of 5 events for next 3 months
		now = datetime.now()
		events_list = EventSummarySerializer(queryset.all()[:10], many=True).data
		events_by_month = []

		start_date = [now.year, now.month]
		for i in range(3):
			end_date = [start_date[0], start_date[1] + 1]


			if start_date[1] == 13:
				start_date[0] = start_date[0] + 1
				start_date[1] = 1

				end_date[0] = start_date[0] + 1
				end_date[1] = 1


			month_start = datetime(start_date[0], start_date[1], 1)
			month_end = datetime(end_date[0], end_date[1], 1) if now.month - i+1 <= 12 else now
			month_str = month_start.strftime("%B")

			events_by_month.append({
				"type": month_str,
				"data": EventSummarySerializer(
					queryset.filter(
						date_time__gte=month_start,
						date_time__lt=month_end
					).order_by("-date_time")[:5],
					many=True
				).data,
				"stats": {
					"Stat 1": 80,
					"Stat 2": 80,
					"Stat 3": 80,
					"Stat 4": 80,
				}
			})

			start_date[1] = start_date[1] + 1


		response_data["stats"] = {
			"Stat 1": ["Lorem ipsum dolor", 80],
			"Stat 2": ["Lorem ipsum dolor", 65],
			"Stat 3": ["Lorem ipsum dolor", 12],
			"Stat 4": ["Lorem ipsum dolor", 91],
		} 
		response_data["events"] = {
			"all": events_list,
			"byMonth": events_by_month,
		}


		return Response(response_data, status=status.HTTP_200_OK)


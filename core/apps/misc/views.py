from rest_framework import (
	generics,
	status,
	pagination,
	mixins,
	viewsets,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.event.serializers import (
	EventSerializer,
	EventSummarySerializer,
)
from core.apps.event.models import (
	Event,
)
from core.apps.misc.field_choices import (
	EventStatuses,
)



class DashboardView(generics.GenericAPIView):

	def get(self, request, *args, **kwargs):
		queryset = Event.objects.filter(coordinator=request.user).distinct()
		response_data = {
			"stats": None,
			"events": None,
		}

		# Set of 5 events by rank
		# events_list = EventSummarySerializer(queryset.all()[:10], many=True).data
		events_by_event_status = []

		for i, event_status in enumerate(EventStatuses.choices):
			events_by_event_status.append({
				"type": event_status[1],
				"data": EventSummarySerializer(
					queryset.filter(
						status=event_status[0]
					).order_by("-title")[:5],
					many=True
				).data,
				"stats": {
					"Stat 1": 80,
					"Stat 2": 80,
					"Stat 3": 80,
					"Stat 4": 80,
				}
			})


		response_data["stats"] = {
			"Stat 1": ["Lorem ipsum dolor", 80],
			"Stat 2": ["Lorem ipsum dolor", 65],
			"Stat 3": ["Lorem ipsum dolor", 12],
			"Stat 4": ["Lorem ipsum dolor", 91],
		} 
		response_data["events"] = events_by_event_status

		response_data["event"] = {
			**EventSerializer(queryset.filter(status=EventStatuses.PLANNING).exclude(task=None)[0]).data
		}

		return Response(response_data, status=status.HTTP_200_OK)


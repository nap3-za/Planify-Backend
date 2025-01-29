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
		queryset = Event.objects.filter(event__coordinator=request.user).distinct()
		response_data = {
			"stats": None,
			"events": None,
		}

		# Set of 5 events by rank
		events_list = EventSummarySerializer(queryset.all()[:10], many=True).data
		events_by_rank = {}

		for i, status in enumerate(EventStatuses.choices):
			events_by_status[f"type_{i+1}"] = {
				"type": status[1],
				"data": EventSummarySerializer(
					queryset.filter(
						status=status[0]
					).order_by("-name")[:5],
					many=True
				).data
			}
			events_by_rank[f"type_{i+1}"]["stats"] = {
				"Stat 1": 80,
				"Stat 2": 80,
				"Stat 3": 80,
				"Stat 4": 80,
			}


		response_data["stats"] = {
			"Stat 1": 80,
			"Stat 2": 80,
			"Stat 3": 80,
			"Stat 4": 80,
		} 
		response_data["events"] = {
			"all": events_list,
			**events_by_rank,
		}

		response_data["event"] = {
			**EventSerializer(queryset.filter(status=EventStatuses.PLANNING)[0]).data
		}

		return Response(response_data, status=status.HTTP_200_OK)


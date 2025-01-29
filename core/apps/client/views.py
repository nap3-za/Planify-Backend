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
	ClientSerializer,
	ClientSummarySerializer,
)
from .models import (
	Client,
)
from core.apps.misc.field_choices import (
	ClientRanks,
)


class ClientViewSetPagination(pagination.PageNumberPagination):
	page_size = 5
	page_size_query_param = "size"
	max_page_size = 5

class ClientViewSet(viewsets.ModelViewSet):

	queryset = Client.objects.all()
	serializer_class = ClientSerializer
	pagination_class = ClientViewSetPagination

	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		queryset = queryset.filter(client__coordinator=request.user).distinct()

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



class DashboardView(generics.GenericAPIView):

	def get(self, request, *args, **kwargs):
		queryset = Client.objects.filter(client__coordinator=request.user).distinct()
		response_data = {
			"stats": None,
			"clients": None,
		}

		# Set of 5 clients by rank
		clients_list = ClientSummarySerializer(queryset.all()[:10], many=True).data
		clients_by_rank = {}

		for i, rank in enumerate(ClientRanks.choices):
			clients_by_rank[f"type_{i+1}"] = {
				"type": rank[1],
				"data": ClientSummarySerializer(
					queryset.filter(
						rank=rank[0]
					).order_by("-name")[:5],
					many=True
				).data
			}
			clients_by_rank[f"type_{i+1}"]["stats"] = {
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
		response_data["clients"] = {
			"all": clients_list,
			**clients_by_rank,
		}


		return Response(response_data, status=status.HTTP_200_OK)


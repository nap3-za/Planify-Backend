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
)
from .models import (
	Client,
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
		queryset = queryset.filter(event__coordinator=request.user).distinct()

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





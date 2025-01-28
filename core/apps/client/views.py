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




from django.conf import settings
from rest_framework import serializers

from .models import (
	Client,
)


class ClientSerializer(serializers.ModelSerializer):
	rank_display 					= serializers.CharField(source="get_rank_display", read_only=True)
	status_display 					= serializers.CharField(source="get_status_display", read_only=True)
	
	class Meta:
		model = Client
		fields = (
			"id",
			"name",
			"code",
			"details",
			"rank",
			"status",
			"relational_timestamp",

			# Display
			"rank_display",
			"status_display",
		)

		read_only_fields = (
			"id",
			"rank_display",
			"status_display",
		)
	
	def update(self, instance, validated_data):
		instance = instance.update(**validated_data)
		return instance
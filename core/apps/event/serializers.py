from django.conf import settings
from rest_framework import serializers

from .models import (
	Event,
	Task,
)


class TaskSerializer(serializers.ModelSerializer):
	priority_display 					= serializers.CharField(source="get_priority_display", read_only=True)
	status_display 					= serializers.CharField(source="get_status_display", read_only=True)
	
	class Meta:
		model = Task
		fields = (
			"id",
			"details",
			"status",
			"priority",
			"due_date",

			# Display
			"priority_display",
			"status_display",

			# Relational
			"event",
		)

		read_only_fields = (
			"id",
			"priority_display",
			"status_display",
		)

		depth = 1
	
	def update(self, instance, validated_data):
		instance = instance.update(**validated_data)
		return instance

class TaskSummarySerializer(serializers.ModelSerializer):
	priority_display 					= serializers.CharField(source="get_priority_display", read_only=True)
	status_display 					= serializers.CharField(source="get_status_display", read_only=True)
	
	class Meta:
		model = Task
		fields = (
			"id",
			"details",
			"due_date",

			# Display
			"priority_display",
			"status_display",
		)

		read_only_fields = (
			"id",
			"priority_display",
			"status_display",
		)


class TaskSerializerField(serializers.RelatedField):
	def to_representation(self, value):
		serialized_tasks = []
		for task in value.all()[:5]:
			serialized_tasks.append(TaskSummarySerializer(task).data)

		return serialized_tasks
				

class EventSerializer(serializers.ModelSerializer):
	priority_display 					= serializers.CharField(source="get_priority_display", read_only=True)
	event_type_display 					= serializers.CharField(source="get_event_type_display", read_only=True)
	status_display 						= serializers.CharField(source="get_status_display", read_only=True)
	bill_status_display 				= serializers.CharField(source="get_bill_status_display", read_only=True)

	tasks 								= TaskSerializer(read_only=True, many=True, source="get_tasks")

	class Meta:
		model = Event
		fields = (
			"id",
			"title",
			"code",
			"details",
			"priority",
			"event_type",
			"status",
			"bill",
			"bill_status",
			"date_time",
			"duration",

			"tasks",

			# Display
			"priority_display",
			"event_type_display",
			"status_display",
			"bill_status_display",

			# Relational
			"coordinator",
			"client"
		)
		read_only_fields = (
			"id",
			"priority_display",
			"event_type_display",
			"status_display",
			"bill_status_display",
		)

		depth = 1

	def update(self, instance, validated_data):
		instance = instance.update(**validated_data)
		return instance	

class EventSummarySerializer(serializers.ModelSerializer):
	priority_display 					= serializers.CharField(source="get_priority_display", read_only=True)
	event_type_display 					= serializers.CharField(source="get_event_type_display", read_only=True)
	status_display 					= serializers.CharField(source="get_status_display", read_only=True)
	bill_status_display 					= serializers.CharField(source="get_bill_status_display", read_only=True)

	tasks 								=  TaskSerializerField(read_only=True)


	class Meta:
		model = Event
		fields = (
			"id",
			"title",
			"code",
			"date_time",
			"duration",

			# Display
			"priority_display",
			"event_type_display",
			"status_display",
			"bill_status_display",

			"tasks",

			# Relational
			"client"
		)
		read_only_fields = (
			"id",
			"priority_display",
			"event_type_display",
			"status_display",
			"bill_status_display",
		)

		depth = 1




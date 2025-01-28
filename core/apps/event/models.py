from django.db import models
from django.db.models import Q

from core.apps.misc.field_choices import (
	PriorityChoices,
	EventTypes,
	EventStatuses,
	BillStatuses,
	TaskStatuses,
	PriorityChoices,
)


class EventQuerySet(models.QuerySet):
	
	def search(self, query=None):
		if query == None:
			return self.none()
		lookups += Q(Q(title__icontains=query))
		return self.filter(lookups)

class Event(models.Model):
	
	class EventManager(models.Manager):

		def create(self, 
				coordinator,
				client,
				title,
				code,
				details,
				priority,
				event_type,
				status,
				bill,
				bill_status,
				date_time,
				duration,
			):
			model = self.model(
				coordinator=coordinator,
				client=client,
				title=title,
				code=code,
				details=details,
				priority=priority,
				event_type=event_type,
				status=status,
				bill=bill,
				bill_status=bill_status,
				date_time=date_time,
				duration=duration,
			)
			model.save(using=self._db)
			return model

		def get_queryset(self):
			return EventQuerySet(self.model, using=self._db)

		def search(self, query=None):
			return self.get_queryset().search(query=query)

		def by_coordinator(self, coordinator):
			return self.all().filter(coordinator=coordinator)

	coordinator 						= models.ForeignKey(
		"account.Account",
		related_name="events",
		related_query_name="event",
		on_delete=models.SET_NULL,
		null=True,
	)
	client 								= models.ForeignKey(
		"client.Client",
		related_name="events",
		related_query_name="event",
		on_delete=models.SET_NULL,
		null=True,
	)

	title 						= models.CharField(verbose_name="title", max_length=125, blank=False)
	code 						= models.CharField(verbose_name="code", max_length=5, unique=True, blank=False)
	details						= models.TextField(blank=True)

	priority 					= models.CharField(verbose_name="priority", choices=PriorityChoices.choices, default=PriorityChoices.MEDIUM, max_length=3, blank=False) 
	event_type 					= models.CharField(verbose_name="event type", choices=EventTypes.choices, max_length=3, default=EventTypes.OTHER, blank=False)
	status 						= models.CharField(verbose_name="status", choices=EventStatuses.choices, max_length=3, default=EventStatuses.CONSULTATION, blank=False)

	bill						= models.DecimalField(verbose_name="bill", max_digits=9, decimal_places=2, default=0.00, null=False)
	bill_status 				= models.CharField(verbose_name="bill status", choices=BillStatuses.choices, max_length=3, default=BillStatuses.UNSETTLED, blank=False)

	date_time					= models.DateTimeField(auto_now_add=False, null=True)
	duration 					= models.DurationField(null=True)

	timestamp					= models.DateTimeField(auto_now_add=True)

	objects = EventManager()


	def __str__(self):
		return f"{self.id}"


	def update(self, **kwargs):
		Event.objects.filter(id=self.id).update(**kwargs)
		return Event.objects.get(id=self.id)


class TaskQuerySet(models.QuerySet):
	
	def search(self, query=None):
		if query == None:
			return self.none()
		lookups += Q(Q(details__icontains=query))
		return self.filter(lookups)

class Task(models.Model):
	
	class TaskManager(models.Manager):

		def create(self,
				event,
				details,
				status,
				priority,
				due_date,
			):
			model = self.model(
				event=event,
				details=details,
				status=status,
				priority=priority,
				due_date=due_date,
			)
			model.save(using=self._db)
			return model

		def get_queryset(self):
			return TaskQuerySet(self.model, using=self._db)

		def search(self, query=None):
			return self.get_queryset().search(query=query)


	event  						= models.ForeignKey(
		"event.Event",
		related_name="tasks",
		related_query_name="task",
		on_delete=models.SET_NULL,
		null=True,
	)

	details 						= models.CharField(verbose_name="details", max_length=125, blank=False)
	status 							= models.CharField(verbose_name="status", choices=TaskStatuses.choices, default=TaskStatuses.NOT_DONE, max_length=3, blank=False) 
	priority 						= models.CharField(verbose_name="priority", choices=PriorityChoices.choices, default=PriorityChoices.MEDIUM, max_length=3, blank=False) 

	due_date 						= models.DateTimeField(verbose_name="due date", auto_now_add=False, null=True)

	timestamp						= models.DateTimeField(auto_now_add=True)

	objects = TaskManager()


	def __str__(self):
		return f"{self.id}"
		

	def update(self, **kwargs):
		Task.objects.filter(id=self.id).update(**kwargs)
		return Task.objects.get(id=self.id)

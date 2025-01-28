from django.db import models
from django.db.models import Q

from core.apps.misc.field_choices import (
	ClientRanks,
	ClientStatuses,
)


class ClientQuerySet(models.QuerySet):
	
	def search(self, query=None):
		if query == None:
			return self.none()
		lookups += Q(Q(name__icontains=query))
		return self.filter(lookups)

class Client(models.Model):
	
	class ClientManager(models.Manager):

		def create(self, 
				name,
				code,
				details,
				rank,
				status,
				relation_timestamp,
			):
			model = self.model(
				name=name,
				code=code,
				details=details,
				rank=rank,
				status=status,
				relation_timestamp=relation_timestamp,
			)
			model.save(using=self._db)
			return model

		def get_queryset(self):
			return ClientQuerySet(self.model, using=self._db)

		def search(self, query=None):
			return self.get_queryset().search(query=query)

	name  						= models.CharField(verbose_name="name", max_length=125, blank=False) 
	code  						= models.CharField(verbose_name="code", max_length=5, blank=False) 
	details 					= models.TextField(blank=True)

	rank 						= models.CharField(verbose_name="rank", choices=ClientRanks.choices, default=ClientRanks.AVERAGE, max_length=3, blank=False)
	status 						= models.CharField(verbose_name="status", choices=ClientStatuses.choices, default=ClientStatuses.ACTIVE, max_length=3, blank=False)

	relation_timestamp			= models.DateField(verbose_name="relation timestamp", null=True)

	timestamp					= models.DateTimeField(auto_now_add=True)

	objects = ClientManager()


	def __str__(self):
		return f"{self.name}"


	def update(self, **kwargs):
		Client.objects.filter(id=self.id).update(**kwargs)
		return Client.objects.get(id=self.id)
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Genders(TextChoices):
	MALE = "MLE", _("Male")
	FEMALE = "FML", _("Female")
	NON_BINARY = "NBN", _("Non-binary")


class PriorityChoices(TextChoices):
	HIGH = "HIG", _("High")
	MEDIUM = "MED", _("Medium")
	LOW = "LOW", _("Low")

class EventTypes(TextChoices):
	OTHER = "OTH", _("Other")
	WEDDING = "WED", _("Wedding")
	BIRTHDAY_PART = "BTP", _("Birthday Party")
	GRADUATION = "GRA", _("Graduation")

class EventStatuses(TextChoices):
	CONSULTATION = "CON", _("Consulation")
	PLANNING = "PLA", _("Planning")
	DONE = "DON", _("Done")

class BillStatuses(TextChoices):
	UNSETTLED = "UNS", _("Unsettled")
	INVOICE_SENT = "IVS", _("Invoice sent")
	SETTLED = "SET", _("Settled")

class TaskStatuses(TextChoices):
	NOT_DONE = "NDN", _("Not done")
	IN_PROGRESS = "INP", _("In progress")
	DONE = "DON", _("Done")


class ClientRanks(TextChoices):
	AVERAGE = "AVG", _("Average")
	GOOD = "GDD", _("Good")
	BAD = "BAD", _("Bad")

class ClientStatuses(TextChoices):
	ACTIVE = "ACT", _("Active")
	LEGACY = "LEG", _("Legacy")
	INACTIVE = "ICT", _("Inactive")
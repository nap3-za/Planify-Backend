from datetime import datetime, timedelta
import random
from core.apps.client.models import Client
from core.apps.event.models import Event, Task  # Replace 'myapp' with your actual app name
from core.apps.account.models import Account

account = Account.objects.all()[0]

# Sample data for generating random strings
def random_string(length=5):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqyrstuvwxyz1234567890', k=length))


client_instances = Client.objects.all()
days = [15, 30, 60, 90, 115]

# Create Event instances using some Client instances
for i, client in enumerate(client_instances[:5]):
    for priority in ["HIG", "MED", "LOW"]:
        for event_type in ["OTH", "WED", "BTP", "GRA"]:
            for status in ["CON", "PLA", "DON"]:
                for bill_status in ["UNS", "IVS", "SET"]:
                    for day in days:
                        try:
                            Event.objects.create(
                                coordinator=account,  # Replace with actual coordinator ID or keep as 0 if not available
                                client=client,
                                title=f"Event Title {i}",
                                code=random_string(),
                                details=f"Details for event {i}",
                                priority=priority,
                                event_type=event_type,
                                status=status,
                                bill=round(random.uniform(100, 1000), 2),
                                bill_status=bill_status,
                                date_time=datetime.now() + timedelta(days=day),
                                duration=timedelta(hours=random.randint(1, 8))
                            )
                        except:
                            print("Clash")



# Create Task instances for some Events
for event in Event.objects.all()[:15]:  # Replace 10 with desired number of events
    for status in ["NDN", "INP", "DON"]:
        for priority in ["HIG", "MED", "LOW"]:
            Task.objects.create(
                event=event,
                details=f"Task details for event {event.id}",
                status=status,
                priority=priority,
                due_date=datetime.now() + timedelta(days=random.randint(1, 30))
            )

print("Instances created successfully!")


# Create Client instances
# client_instances = []
# for i in range(9):
#     for rank in ["AVG", "GDD", "BAD"]:
#         for status in ["ACT", "LEG", "ICT"]:
#             client = Client.objects.create(
#                 name=f"Client {i}",
#                 code=random_string(),
#                 details=f"Details for client {i}",
#                 rank=rank,
#                 status=status,
#                 relation_timestamp=datetime.now().date() - timedelta(days=random.randint(100, 1000))
#             )
#             client_instances.append(client)
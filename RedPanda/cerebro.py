import os
import sys
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RedPanda.settings")
django.setup()

from django.db import models
from iot_hub.models import DataSource, Variable, Event


events = Event.objects.filter(data_variable="e7737df9-081f-482d-931d-ca2b1f49d19f")
print events
print events[1].operand

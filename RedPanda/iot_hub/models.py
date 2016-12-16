from __future__ import unicode_literals

from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class DataSource(models.Model):
	name = models.CharField(max_length=50, default="")
	label = models.CharField(max_length=50)
	description = models.TextField(max_length=250)
	source_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	create_date = models.DateField(auto_now_add=True)
	edition_date = models.DateField(auto_now=True)
	def self_id(self):
		return self.name + '-' + str(self.source_id)[-4:]
	def __unicode__(self):
		return self.self_id()

class Variable(models.Model):
	name = models.CharField(max_length=50, default="")
	unit = models.CharField(max_length=50)
	description = models.CharField(max_length=250)
	icon = models.CharField(max_length=50)
	var_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
	def source_short_id(self):
		return self.data_source.self_id()
	def self_id(self):
		return self.name + '-' + str(self.var_id)[-4:]
	def __unicode__(self):
		return self.self_id()

class VarValue(models.Model):
	value = models.FloatField()
	timestamp = models.DateTimeField('date published', default=timezone.now)
	location = models.CharField(max_length=100)
	variable = models.ForeignKey(Variable, on_delete=models.CASCADE)

class Event(models.Model):
	MORE_THAN = 'MT'
	LESS_THAN = 'LT'
	EQUAL = 'EQ'
	MORE_EQUAL = 'ME'
	LESS_EQUAL = 'LE'

	SEND_SMS = "SMS"
	SEND_TELEGRAM = "TEL"
	SEND_MAIL = "EMA"
	SET_VARIABLE = "SET"

	ACTION_CHOICES = (
		(SEND_SMS, "Send an SMS"),
		(SEND_TELEGRAM, "Send a telegram message"),
		(SEND_MAIL, "Send an email"),
		(SET_VARIABLE, "Set a variable"),
	) 

	COMPARE_CHOICES = (
		(MORE_THAN, 'More than'),
		(LESS_THAN, 'Less than'),
		(EQUAL, 'Equal'),
		(MORE_EQUAL, 'More or equal than'),
		(LESS_EQUAL, 'Less or equal than'),
	)

	name = models.CharField(max_length=50)
	description = models.TextField(max_length=250, null=True, blank=True)
	data_source = models.ForeignKey(DataSource, db_index=True, null=False, blank=False)
	data_variable = models.ForeignKey(Variable, null=False, blank=False)
	operand = models.CharField(
		max_length=2,
		choices=COMPARE_CHOICES,
		default=EQUAL,
	)
	compare_value = models.FloatField()
	action = models.CharField(
		max_length=3,
		choices=ACTION_CHOICES,
		default=SET_VARIABLE,
	)
	set_data_source = models.ForeignKey(DataSource, related_name='%(class)s_requests_created', null=True, blank=True)
	set_data_variable = models.ForeignKey(Variable, related_name='%(class)s_requests_created', null=True, blank=True)
	value_set = models.FloatField(null=True, blank=True)
	telegram_id = models.CharField(max_length = 20, null=True, blank=True)
	def self_id(self):
		return self.name + '(' + self.data_source.self_id() + ',' + self.data_variable.self_id() + ':' + self.operand + ',' + str(self.compare_value) + ')'
	def __unicode__(self):
		return self.self_id()

class Widget(models.Model):
	CHART = "CHT"
	METRIC = "MTC"
	INDICATOR = "IND"
	BUTTON = "BUTN"

	TYPE_CHOICES = (
		(CHART, "Chart"),
		(METRIC, "Metric"),
		(INDICATOR, "Indicator"),
		(BUTTON, "Button")
	)

	name = models.CharField(max_length=50)
	widget_type = models.CharField(
		max_length=3,
		choices=TYPE_CHOICES,
		default=CHART,
		)
	data_variable = models.ForeignKey(Variable, null=False, blank=False)
	datapoints = models.IntegerField()
	def __unicode__(self):
		return self.name
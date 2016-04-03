from __future__ import unicode_literals

from django.db import models
from authentication.models import Account

# Create your models here.
USER_ID_TYPE = (
    ('0', 'CC'),
    ('1', 'CE'),
    ('2', 'PASAPORTE'),
)

class Rates(models.Model):
	min = models.IntegerField()
	max = models.IntegerField()
	commission_sender =models.FloatField()
	commission_correspondent_receiver =models.FloatField()
	commission_correspondent_receiver =models.FloatField()
	type = models.CharField(max_length=1)

class Bank(models.Model):
    cod = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

class Municipality (models.Model):
    dane_code = models.IntegerField()
    name=models.CharField(max_length=50)

class Town(models.Model):
    dane_code = models.IntegerField()
    name=models.CharField(max_length=50)
    municipality = models.ForeignKey(Municipality, related_name='municipality')

class Document(models.Model):
    user = models.ForeignKey(Account, related_name='user')
    type = models.CharField(max_length=1, choices=USER_ID_TYPE)
    video_original=models.FileField()
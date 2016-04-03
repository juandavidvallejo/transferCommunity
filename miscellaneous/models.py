from __future__ import unicode_literals

from django.db import models

# Create your models here.


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



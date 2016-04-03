from django.db import models
from authentication.models import Account
from authentication.models import DocumentType,Province,City

class Giros(models.Model):
	sender = models.ForeignKey(Account, related_name='sender')
	receiver = models.ForeignKey(Account, related_name='receiver')
	correspondent = models.ForeignKey(Account, related_name='correspondent')
	amount = models.PositiveIntegerField()
	commission_total = models.FloatField()
	commission_correspondent_receiver = models.FloatField()
	commission_correspondent_delevery = models.FloatField()
	created_at = models.DateTimeField()
	state = models.CharField(max_length=200, null=True)
	mobile_receiver = models.CharField(max_length=40, blank=True)
	first_name_receiver = models.CharField(max_length=40, blank=True)
	last_name_receiver = models.CharField(max_length=40, blank=True)
	document_type_receiver = models.ForeignKey(DocumentType)
	document_receiver=models.CharField(max_length=40, blank=True)
	province_receiver=models.ForeignKey(Province, related_name='province_receiver')
	province_delevery=models.ForeignKey(Province, related_name='province_delevery')
	city_receiver=models.ForeignKey(City, related_name='city_receiver')
	city_delevery=models.ForeignKey(City, related_name='city_delevery')
	correspondent_receiver=models.ForeignKey(Account, related_name='correspondent_rece')
	correspondent_delevery=models.ForeignKey(Account, related_name='correspondent_dele')
	received_correspondent= models.BooleanField(default=False)
	received_receiver=models.BooleanField(default=False)
	received_at = models.DateTimeField()


	def __unicode__(self):
		return '{0}'.format(self.sender)


class GirosHistoricos(models.Model):
	giro = models.ForeignKey(Giros, default='null')
	received_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '{0}'.format(self.giro)
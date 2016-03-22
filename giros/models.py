from django.db import models
from authentication.models import Account

class Giros(models.Model):
	sender = models.ForeignKey(Account, related_name='sender')
	receiver = models.ForeignKey(Account, related_name='receiver')
	correspondent = models.ForeignKey(Account, related_name='correspondent')
	amount = models.PositiveIntegerField()
	commission = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	state = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return '{0}'.format(self.sender)


class GirosHistoricos(models.Model):
	giro = models.ForeignKey(Giros, default='null')
	received_at = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return '{0}'.format(self.giro)
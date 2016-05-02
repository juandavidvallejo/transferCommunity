from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from miscellaneous.models import Bank
import psycopg2
import os

conn=psycopg2.connect(host='transfercommunity.cbvfzor8r6v6.us-west-2.rds.amazonaws.com', user='postgres', password='1nt3gr4d0r',database='transfercommunity')

VALIDATION_STATE = (
    ('0', 'NO'),
    ('1', 'SENT'),
    ('2', 'RECEIVED'),
)
USER_ID_TYPE = (
    ('0', 'CC'),
    ('1', 'CE'),
    ('2', 'PASAPORTE'),
)

USER_TYPE = (
    ('0', 'receiver'),
    ('1', 'sender'),
    ('2', 'any'),
)

class DocumentType(models.Model):
    name = models.CharField(max_length=200, null=True)

class Province(models.Model):
    dane_code = models.IntegerField()
    name = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ('name',)

class City(models.Model):
    dane_code = models.IntegerField()
    name = models.CharField(max_length=200, null=True)
    province = models.ForeignKey(Province)

    class Meta:
        ordering = ('name',)

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username'), first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'), mobile_number=kwargs.get('mobile_number'),  document_type=kwargs.get('document_type'), num_id=kwargs.get('num_id')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account

class Account(AbstractBaseUser):

    document_type = models.ForeignKey(DocumentType)
    num_id=models.CharField(max_length=40, blank=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    mobile_number = models.CharField(max_length=40, blank=True)
    phone_number =models.CharField(null=True, max_length=40, blank=True)

    email = models.EmailField(unique=True)
    location = models.CharField(null=True, max_length=40, blank=True)
    address =models.CharField(null=True, max_length=200, blank=True)
    city = models.ForeignKey(City, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, blank=True)

    rol = models.CharField(null=True, max_length=45,  blank=True)

    correspondent_type = models.CharField(null=True, max_length=20, blank=True, choices=USER_TYPE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    genere = models.CharField(null=True, max_length=40, blank=True)
    income_source=models.CharField(null=True, max_length=400, blank=True)

    credit_card=models.CharField(null=True, max_length=16, blank=True)
    valid_code_credit_card=models.CharField(null=True, max_length=3, blank=True)

    SMS_code=models.CharField(null=True, max_length=8, blank=True)
    sender_status=models.BooleanField(default=True)
    correspondent_status=models.BooleanField(default=False)
    correspondent_sender=models.BooleanField(default=False)
    correspondent_receiver=models.BooleanField(default=False)
    latitude=models.FloatField(null=True, blank=True)
    longitude=models.FloatField(null=True, blank=True)

    bank_account=models.IntegerField(null=True, blank=True)
    bank=models.ForeignKey(Bank, null=True, blank=True)

    max_mount_receiver=models.IntegerField(null=True, blank=True)
    max_mount_delivery=models.IntegerField(null=True, blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email_validation = models.CharField(null=True, max_length=20, choices=VALIDATION_STATE)
    mobile_validation = models.CharField(null=True, max_length=20, choices=VALIDATION_STATE)


    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def getDistancia(self, longitud, latitud, monto, ciudad):
        cursor = conn.cursor()
        cursor.execute("SELECT SQRT(POW(%s-authentication_account.longitude,2)+POW(%s-authentication_account.latitude,2)) AS distancia FROM authentication_account INNER JOIN authentication_city ON authentication_account.city_id=authentication_city.id WHERE authentication_account.max_mount_receiver>=%s AND authentication_city.dane_code=%s AND authentication_account.id=%s ORDER BY distancia LIMIT 5;", (longitud,latitud,monto,ciudad, self.pk))
        distancia = cursor.fetchone()
        cursor.close()
        return distancia


class Document(models.Model):
    user = models.ForeignKey(Account, related_name='user')
    type = models.CharField(max_length=1, choices=USER_ID_TYPE)
    image_path =models.FileField()
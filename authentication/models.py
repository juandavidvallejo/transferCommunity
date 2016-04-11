from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from miscellaneous.models import Bank
import psycopg2
import os

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



class DocumentType(models.Model):
    name = models.CharField(max_length=200, null=True)

class Province(models.Model):
    dane_code = models.IntegerField()
    name = models.CharField(max_length=200, null=True)

class City(models.Model):
    dane_code = models.IntegerField()
    name = models.CharField(max_length=200, null=True)
    province = models.ForeignKey(Province)

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username'), first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'), mobile_number=kwargs.get('mobile_number'), location=kwargs.get('location'), rol=kwargs.get('rol'), genere=kwargs.get('genere'), document_type=kwargs.get('document_type'), city=kwargs.get('city')
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
    phone_number =models.CharField(max_length=40, blank=True)

    email = models.EmailField(unique=True)
    location = models.CharField(max_length=40, blank=True)
    address =models.CharField(max_length=200, blank=True)
    city = models.ForeignKey(City)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, blank=True)

    rol = models.CharField(max_length=45,  blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    genere = models.CharField(max_length=40, blank=True)
    income_source=models.CharField(max_length=400, blank=True)

    credit_card=models.CharField(max_length=16, blank=True)
    valid_code_credit_card=models.CharField(max_length=3, blank=True)

    SMS_code=models.CharField(max_length=8, blank=True)
    sender_status=models.BooleanField(default=True)
    correspondent_status=models.BooleanField(default=False)
    correspondent_sender=models.BooleanField(default=False)
    correspondent_receiver=models.BooleanField(default=False)
    latitude=models.FloatField(blank=True)
    longitude=models.FloatField(blank=True)

    bank_account=models.IntegerField(blank=True)
    bank=models.ForeignKey(Bank, blank=True)

    max_mount_receiver=models.IntegerField(blank=True)
    max_mount_delivery=models.IntegerField(blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email_validation = models.CharField(max_length=20, choices=VALIDATION_STATE)
    mobile_validation = models.CharField(max_length=20, choices=VALIDATION_STATE)


    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def get_params(self):
        prueba = request.GET.get['longitud']
        print prueba
        #return self

    def getDistancia(self):
        conn=psycopg2.connect(host='transfercommunity.cbvfzor8r6v6.us-west-2.rds.amazonaws.com', user='postgres', password='1nt3gr4d0r',database='transfercommunity')
        cursor = conn.cursor()
        cursor.execute("SELECT SQRT(POW(4.6021898201365055-authentication_account.longitude,2)+POW(-74.0654952957932-authentication_account.latitude,2)) AS distancia FROM authentication_account INNER JOIN authentication_city ON authentication_account.city_id=authentication_city.id WHERE authentication_account.max_mount_receiver>=500000 ORDER BY distancia LIMIT 5;")
        #cursor.execute("SELECT SQRT(POW(4.6021898201365055-authentication_account.longitude,2)+POW(-74.0654952957932-authentication_account.latitude,2)) AS distancia FROM authentication_account INNER JOIN authentication_city ON city_id=authentication_city.id WHERE max_mount_receiver>=500000 AND authentication_city.dane_code=587 ORDER BY distancia LIMIT 5;")
        #cursor.execute("SELECT id FROM authentication_account WHERE id=1;"), (longitud,latitud,monto,ciudad,)
        distancia = cursor.fetchone()
        #print distancia
        #cursor.close()
        #conn.close()
        return distancia

class Document(models.Model):
    user = models.ForeignKey(Account, related_name='user')
    type = models.CharField(max_length=1, choices=USER_ID_TYPE)
    image_path =models.FileField()
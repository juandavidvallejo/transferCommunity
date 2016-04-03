from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from miscellaneous.models import Bank


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
    latitude=models.FloatField()
    longitude=models.FloatField()

    bank_account=models.IntegerField()
    bank=models.ForeignKey(Bank)

    max_mount_receiver=models.IntegerField()
    max_mount_delivery=models.IntegerField()

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


class Document(models.Model):
    user = models.ForeignKey(Account, related_name='user')
    type = models.CharField(max_length=1, choices=USER_ID_TYPE)
    image_path =models.FileField()
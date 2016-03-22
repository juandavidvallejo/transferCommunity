from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class DocumentType(models.Model):
    name = models.CharField(max_length=200, null=True)

class Province(models.Model):
    name = models.CharField(max_length=200, null=True)

class City(models.Model):
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
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    mobile_number = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=40, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, blank=True)

    rol = models.CharField(max_length=45,  blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    genere = models.CharField(max_length=40, blank=True)

    document_type = models.ForeignKey(DocumentType)
    city = models.ForeignKey(City)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name


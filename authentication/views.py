from rest_framework import permissions, viewsets, generics
from authentication.models import Account, Province, City
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer, DepartamentoSerializer,MuniciposSerializer, CorresponsalSerializer, CompletaRegistroSerializer, BankSerializer
from django.utils.decorators import method_decorator
from rest_framework.response import Response
import json
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views, permissions
from rest_framework.renderers import JSONRenderer
from miscellaneous.models import Bank
import os
from twilio.rest import TwilioRestClient
import string
import random

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=self.request.GET)
        print self.request.GET
        print serializer.is_valid(), " errores ",serializer.errors

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)
            SMS_code = self.id_generator()
            Account.objects.filter(email=self.request.GET.get('email')).update(SMS_code=SMS_code)
            accountSID = os.environ.get('TWILIO_ACCOUNT_SID')
            authToken = os.environ.get('TWILIO_AUTH_TOKEN')
            twilioCli = TwilioRestClient(accountSID, authToken)
            myTwilioNumber = '+12673383067'
            myCellPhone = ''.join(['+57', self.request.GET.get('mobile_number')])
            message = twilioCli.messages.create(body=SMS_code, from_=myTwilioNumber, to=myCellPhone)
            return Response({
            'status': 'Created',
            'message': 'Account has been successfully created.'
        },status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(6))

class LoginView(views.APIView):
    def post(self, request, format=None):
        #data = json.loads(request.body)

        #email = data.get('email', None)
        #password = data.get('password', None)

        email = self.request.GET.get('email')
        password = self.request.GET.get('password')

        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class DepartamentosView(generics.ListAPIView):
    serializer_class = DepartamentoSerializer
    queryset = Province.objects.all()

class DepartamentosIdView(generics.ListAPIView):
    serializer_class = MuniciposSerializer

    def get_queryset(self):
        dane = self.kwargs['dane']
        return City.objects.filter(province__dane_code=dane)

class ConsultaCorresponsalView(generics.ListAPIView):
    serializer_class = CorresponsalSerializer
    
    def get_serializer_context(self):
        for i in self.request.GET:
            if i == 'longitud':
                longitud = self.request.GET.get('longitud')
            if i == 'latitud':
                latitud = self.request.GET.get('latitud')
            if i == 'monto':
                monto = self.request.GET.get('monto')
            if i == 'ciudad':
                ciudad = self.request.GET.get('ciudad')
        return {'longitud':longitud, 'latitud':latitud, 'monto': monto, 'ciudad': ciudad}

    def get_queryset(self):
        queryset = Account.objects.filter(correspondent_type=0)
        for i in self.request.GET:
            if i == 'tipo':
                tipo = self.request.GET.get('tipo')
                queryset =  queryset.filter(correspondent_type=tipo)
            if i == 'monto':
                monto = self.request.GET.get('monto')
                queryset =  queryset.filter(max_mount_receiver__gte=monto)
            if i == 'ciudad':
                ciudad = self.request.GET.get('ciudad')
                city = City.objects.filter(dane_code=ciudad)
                queryset = queryset.filter(city=city)
        return queryset
        
class CompletaRegistroViewSet(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = CompletaRegistroSerializer
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(self, request, *args, **kwargs)

    def put(self, request):
        email = self.request.GET.get('email')
        city = self.request.GET.get('city')
        address = self.request.GET.get('address')
        phone_number = self.request.GET.get('phone_number')
        genere = self.request.GET.get('genere')
        income_source = self.request.GET.get('income_source')
        bank = self.request.GET.get('bank')
        bank_account = self.request.GET.get('bank_account')
        queryset = Account.objects.filter(email=email).update(city=city, address=address,
            phone_number=phone_number, genere=genere, income_source=income_source,
            bank=bank, bank_account=bank_account)
        return Response({
                    'status': 'Created',
                    'message': 'User created successfully'
                },status=status.HTTP_201_CREATED)

class UsuariosView(generics.ListAPIView):
    serializer_class = CompletaRegistroSerializer
    queryset = Account.objects.all()

class BankView(generics.ListAPIView):
    serializer_class = BankSerializer

    def get_queryset(self):
        queryset = Bank.objects.all().order_by('cod')
        if self.request.GET.get('cod'):
            cod = self.request.GET.get('cod')
            queryset = queryset.filter(cod=cod)
        return queryset

class ValidateCode(views.APIView):

    def post(self, request, format=None):
        code = self.request.GET.get('code')
        email = self.request.GET.get('email')
        account = Account.objects.filter(email=email)
        if account.filter(SMS_code=code).count() > 0:
            return Response({
                'status': 'Validated',
                'message': 'Code was validated successfully'
                }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'Bad request',
            'message': 'Code invalid'
        }, status=status.HTTP_400_BAD_REQUEST)

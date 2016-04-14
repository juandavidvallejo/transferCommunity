from rest_framework import permissions, viewsets, generics
from authentication.models import Account, Province, City
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer, DepartamentoSerializer,MuniciposSerializer, CorresponsalSerializer
from django.utils.decorators import method_decorator
from rest_framework.response import Response
import json
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views, permissions
from rest_framework.renderers import JSONRenderer

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
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        email = data.get('email', None)
        password = data.get('password', None)

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
        

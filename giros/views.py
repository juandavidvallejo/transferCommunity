from django.shortcuts import render
from rest_framework import permissions, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from giros.models import Giros
from giros.permissions import IsSenderOfMoney
from giros.serializers import GirosSerializer
import json


class GirosViewSet(viewsets.ModelViewSet):
    queryset = Giros.objects.order_by('-created_at')
    serializer_class = GirosSerializer
    #renderer_classes = [JSONRenderer]

    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #     return (permissions.IsAuthenticated(), IsSenderOfMoney(),)


    def perform_create(self, serializer):
        instance = serializer.save(sender=self.request.user)

        return super(PostViewSet, self).perform_create(serializer)

class AccountGirosViewSet(viewsets.ViewSet):
    queryset = Giros.objects.select_related('author').all()
    serializer_class = GirosSerializer

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(sender__username=account_username)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

class GirosView(generics.ListCreateAPIView):
    queryset = Giros.objects.all()
    serializer_class = GirosSerializer

    def get_context(self):
        sender = self.request.GET.get('usuario')
        amount = self.request.GET.get('monto')
        receiver = self.request.GET.get('usuarioReceptor')
        mobile_receiver = self.request.GET.get('celular')
        document_type_receiver = self.request.GET.get('tipoDoc')
        document_receiver = self.request.GET.get('documento')
        city_receiver = self.request.GET.get('municipio')
        correspondent_receiver = self.request.GET.get('usuarioCorresponsal')
        commission_total = 5000
        commission_correspondent_delivery = commission_total * 0.4
        commission_correspondent_receiver = commission_total * 0.4
        correspondent_delivery = 1
        data = {'sender':sender, 'amount':amount, 'receiver': receiver, 'mobile_receiver': mobile_receiver, 'document_type_receiver': document_type_receiver, 'document_receiver': document_receiver, 'city_receiver': city_receiver, 'correspondent_receiver': correspondent_receiver, 'commission_total': commission_total, 'commission_correspondent_delivery': commission_correspondent_delivery,'commission_correspondent_receiver': commission_correspondent_receiver, 'correspondent_delivery':correspondent_delivery}
        return Response(data=data)



    def post(self, request):
        request = self.get_context()
        self.serializer_class = GirosSerializer
        return super(GirosView, self).post(request)

        
        # for i in self.request.GET:
        #     if i == 'usuario':
        #         usuario = self.request.GET.get('usuario')
        #     if i == 'monto':
        #         monto = self.request.GET.get('monto')
        #     if i == 'usuarioReceptor':
        #         usuarioReceptor = self.request.GET.get('usuarioReceptor')
        #     if i == 'celular':
        #         celular = self.request.GET.get('celular')
        #     if i == 'tipoDoc':
        #         tipoDoc = self.request.GET.get('tipoDoc')
        #     if i == 'documento':
        #         documento = self.request.GET.get('documento')
        #     if i == 'municipio':
        #         municipio = self.request.GET.get('municipio')
        #     #usuario corresponsal que recibe
        #     if i == 'usuarioCorresponsal':
        #         usuarioCorresponsal = self.request.GET.get('usuarioCorresponsal')
        #return {'sender':usuario, 'monto':monto, 'usuarioReceptor': usuarioReceptor, 'celular': celular, 'tipoDoc': tipoDoc, 'documento': documento, 'municipio': municipio, 'usuarioCorresponsal': usuarioCorresponsal}
    


#iniciarGiro/usuario/monto/usuarioReceptor/celular/tipoDoc/documento/dpto/municipio/tomarDe/usuarioCorresponsal

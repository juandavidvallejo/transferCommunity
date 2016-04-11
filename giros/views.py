from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from giros.models import Giros
from giros.permissions import IsSenderOfMoney
from giros.serializers import GirosSerializer


class GirosViewSet(viewsets.ModelViewSet):
    ##usuario, monto, longitud, latitud, tipo
    queryset = Giros.objects.order_by('-created_at')
    serializer_class = GirosSerializer
    #renderer_classes = [JSONRenderer]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsSenderOfMoney(),)

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
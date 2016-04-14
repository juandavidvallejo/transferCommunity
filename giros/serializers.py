from rest_framework import serializers

from authentication.serializers import AccountSerializer
from giros.models import Giros


class GirosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Giros
        fields = ('id', 'sender', 'amount', 'receiver', 'mobile_receiver','document_type_receiver', 'document_receiver', 
            'city_receiver', 'correspondent_receiver', 'commission_total', 'commission_correspondent_receiver', 'commission_correspondent_delivery','created_at', 'correspondent_delivery')
        read_only_fields = ('id', 'created_at',)

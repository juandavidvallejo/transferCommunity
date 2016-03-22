from rest_framework import serializers

from authentication.serializers import AccountSerializer
from giros.models import Giros


class GirosSerializer(serializers.ModelSerializer):
    sender = AccountSerializer(read_only=True, required=False)
    receiver = AccountSerializer(read_only=True, required=False)
    correspondent = AccountSerializer(read_only=True, required=False)

    class Meta:
        model = Giros
        fields = ('id', 'sender',  'receiver', 'correspondent', 'amount','commission' ,'created_at', 'state')
        read_only_fields = ('id', 'created_at', 'amount')

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(PostSerializer, self).get_validation_exclusions()

        return exclusions + ['sender']
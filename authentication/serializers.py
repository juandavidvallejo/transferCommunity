from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from authentication.models import Account, DocumentType, City, Province

class DocumentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocumentType  
        fields = ('id', 'name')
    
class ProvinceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Province  
        fields = ('id', 'name')

class CitySerializer(serializers.HyperlinkedModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = City  
        fields = ('id', 'name', 'province')

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    document_type = DocumentTypeSerializer()
    city = CitySerializer()


    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'mobile_number', 'location', 'rol', 'genere', 'document_type', 'city','password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance
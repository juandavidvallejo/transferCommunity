from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from authentication.models import Account, DocumentType, City, Province

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType  
        fields = ('id', 'name')
    
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province  
        fields = ('id', 'name')

class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = City  
        fields = ('id', 'name', 'province')

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)


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

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        resource_name = 'departamentos'

class MuniciposSerializer(serializers.ModelSerializer):
    province = DepartamentoSerializer()

    class Meta:
        model = City
        fields = ('id','name', 'dane_code', 'province')

class CorresponsalSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField('descre')


    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'location', 'longitude','latitude','city', 'distance',)   
    
    def descre(self, obj):
        longitud = self.context.get('longitud')
        latitud = self.context.get('latitud')
        monto = self.context.get('monto')
        ciudad = self.context.get('ciudad')
        data = obj.getDistancia(longitud, latitud, monto, ciudad)
        return data
    
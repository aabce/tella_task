from rest_framework import serializers
from .models import Product
from django.contrib.auth import get_user_model


class UserSerializer( serializers.ModelSerializer ):
    url = serializers.SerializerMethodField( read_only=True )

    def get_url( self, obj ):
        request = self.context.get( "request" )
        return obj.get_api_url( request=request )

    class Meta:
        model = get_user_model()
        fields = ( 'url', 'id', 'email', 'first_name', 'last_name', )


class ProductSerializer( serializers.ModelSerializer ):
    url = serializers.SerializerMethodField( read_only=True )
    # id = serializers.IntegerField()

    def get_url( self, obj ):
        request = self.context.get( "request" )
        return obj.get_api_url( request=request )

    class Meta:
        model = Product
        fields = ( 'id', 'url', 'title', 'description', 'features', 'img', )

    def create(self, validated_data):
        product = Product( user=self.context.get( 'user' ), **validated_data )
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.title          = validated_data.pop( 'title', instance.title )
        instance.img            = validated_data.pop( 'img', instance.img )
        instance.description    = validated_data.pop( 'description', instance.description )
        instance.features       = validated_data.pop('features', instance.description)
        instance.save()
        return instance


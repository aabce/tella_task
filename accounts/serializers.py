from accounts.models import Profile, Permission, User
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import IsQuizMaker


class PermissionSerializer( serializers.ModelSerializer ):

    class Meta:
        model  = Permission
        fields = [ 'id', 'name', 'level' ]


class ProfileSerializer( serializers.ModelSerializer ):

    class Meta:
        model  = Profile
        fields = [ 'id', 'rank' ]

class UserSerializer( serializers.ModelSerializer ):
    profile     = ProfileSerializer( required=True )
    permissions = PermissionSerializer( required=False, many=True )
    url         = serializers.SerializerMethodField( read_only=True )

    def get_url( self, obj ):
        request = self.context.get( "request" )
        return obj.get_api_url( request=request )

    class Meta:
        model = User
        fields = ( 'url', 'email', 'first_name', 'last_name', 'profile', 'permissions' )



class PasswordSerializer( serializers.Serializer ):
    url         = serializers.SerializerMethodField( read_only=True )
    id          = serializers.CharField( required=True )
    password    = serializers.CharField( required=True )

    class Meta:
        fields = ('url', 'id', 'password')

    def get_url( self, obj ):
        pass

class UserRegistrationSerializer( serializers.ModelSerializer ):
    profile     = ProfileSerializer( required=False )
    permissions = PermissionSerializer( required=False, many=True )
    url         = serializers.SerializerMethodField( read_only=True )

    class Meta:
        model  = User
        fields = ('url', 'id', 'email', 'first_name', 'last_name', 'password', 'profile', 'permissions')

    def get_url( self, obj ):
        request = self.context.get( "request" )
        return obj.get_api_url( request=request )

    def create( self, validated_data ):
        profile_data        = validated_data.pop( 'profile' )
        permissions_data    = validated_data.pop( 'permissions' )
        password            = validated_data.pop( 'password' )
        
        
        user = User( **validated_data )
        user.set_password( password )
        user.save()
        Profile.objects.create( user=user, **profile_data )
        
        if ( permissions_data ):
            for permission_data in permissions_data:
                Permission.objects.create(user=user, **permission_data)
        
        return user

    def update( self, instance, validated_data ):
        # print( f'VD={ validated_data }' )
        profile_data        = validated_data.pop( 'profile', None )
        permissions_data    = validated_data.pop( 'permissions', None )
        password            = validated_data.pop( 'password', None )

        try:
            profile =  instance.profile
        except Profile.DoesNotExist:
            profile = None
        
        try:
            permissions = instance.permissions
        except Permission.DoesNotExist:
            permissions = None

        instance.email      = validated_data.get( 'email', instance.email )
        instance.password   = validated_data.get( 'password', instance.password )
        instance.first_name = validated_data.get( 'first_name', instance.first_name )
        instance.last_name  = validated_data.get( 'last_name', instance.last_name )


        instance.save()
        # profile.rank = profile_data.get( 'rank', profile.rank )
        # profile.save()

        return instance
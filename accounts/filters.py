from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

class UserFilter( filters.FilterSet ):

    class Meta:
        model = get_user_model()
        fields = {
            'first_name': [ 'icontains' ], 
            'last_name': [ 'icontains' ],
        }
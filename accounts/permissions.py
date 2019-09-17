from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class IsQuizMaker( BasePermission ):


    def has_permission( self, request, view ):
        current_user = self.context['request'].user | None
        
        if ( current_user ):
            print( f'this is user={ current_user }' )
        else:
            print( f'NO user provided' )


        return True
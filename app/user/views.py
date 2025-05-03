"""
views for the user api 
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (UserSerielizer,
                              AuthTokenSerializer)
class CreateUserView(generics.CreateAPIView):
    """create a new user in the system"""
    serializer_class=UserSerielizer  #this will map or serializer with the above api_call()
    #api_call made by the CreateAPIView-->HTTP request with post method.

class CreateTokenView(ObtainAuthToken):
    """create a new auth token for user"""
    serializer_class=AuthTokenSerializer
    #renderer_classes=api_settings.DEFAULT_RENDER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticate user."""
    serializer_class=UserSerielizer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        """retrive and return the authenticated user"""
        return self.request.user

from auth_app.api.serializers import Registrationserializer, LoginParentSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.response import Response
from rest_framework import generics, status
from .token import generate_random_token
class RegistrationView(generics.CreateAPIView):
    """
    API view for user registration.

    Handles the creation of a new user account.
    """
    serializer_class = Registrationserializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.

        :param request: The HTTP request object
        :return: Response containing the created user data or error messages
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False
        host = request.get_host()
        print(serializer.data)
        zahl = generate_random_token()
        print(zahl)
        print(serializer.data['children'])
        print(host)
        code = urlsafe_base64_encode(force_bytes(user.pk))
        print(code)
        

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class LoginParentView(TokenObtainPairView):
    """
    API view for obtaining JWT tokens for parent users.

    Inherits from TokenObtainPairView to provide token generation functionality.
    """
    serializer_class = LoginParentSerializer
    
    
    def post(self, request, *args, **kwargs):
        seralizer = self.get_serializer(data=request.data)
        if not seralizer.is_valid():
            return Response(seralizer.errors, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = seralizer.validated_data['refresh']
        access = seralizer.validated_data['access']
        response = Response({"detail": "Login successfully!","user": {'id': seralizer.user.id,
                                                                      'email': seralizer.user.email, 'role': seralizer.user.role }}
                                                                        ,status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token", value=access, httponly=True, secure=True, samesite="Lax")
        
        response.set_cookie(
            key="refresh_token", value=refresh, httponly=True, secure=True, samesite="Lax")
        return response
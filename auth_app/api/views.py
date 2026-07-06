from rest_framework.response import Response
from rest_framework import generics, status
from auth_app.api.serializers import Registrationserializer


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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
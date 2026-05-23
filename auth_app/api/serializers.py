from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()


class Registrationserializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles creation of a new user account, including:
    - Username
    - Email
    - Password confirmation
    """

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        """
        Meta configuration for Registrationserializer.
        """
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_confirmed_password(self, value):
        """
        Ensure that the confirmed password matches the original password.

        :param value: The confirmed password provided by the user
        :return: The validated confirmed password
        :raises ValidationError: If passwords do not match
        """
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        """
        Validate that the email address is unique.

        :param value: Email address provided by the user
        :return: The validated email
        :raises ValidationError: If the email already exists
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        """
        Create and save a new user instance.

        The password is securely hashed using Django's set_password method.

        :return: The created User instance
        """
        pw = self.validated_data['password']
        username = self.validated_data['username']
        account = User(
            email=self.validated_data['email'],
            username=username
        )
        account.set_password(pw)
        account.save()
        return account


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extended JWT serializer that embeds additional user information
    into the token response.
    """

    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        """
        Validates the login credentials and extends the JWT response.

        Args:
            attrs (dict): The incoming authentication data (e.g. username & password).

        Returns:
            dict: The token response, extended with the user's 'email' and 'id'.
        """
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['id'] = self.user.id
        data['role'] = self.user.role

        return data

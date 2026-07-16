import email

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from auth_app.models import User, Child
from django.contrib.auth import authenticate
from .token import  generate_random_token




class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'name', 'age', 'image', 'password']
        extra_kwargs = {

             'password': {'required': False}
        }
        
        
    
            


class Registrationserializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles creation of a new user account, including:
    - Username
    - Email
    - Password confirmation
    """
    email = serializers.EmailField(required=False, allow_blank=True)
    confirmed_password = serializers.CharField(write_only=True)
    children = ChildSerializer(many=True, required=False)

    class Meta:
        """
        Meta configuration for Registrationserializer.
        """
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password', 'role', 'children']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        role = attrs.get('role')
        email = attrs.get('email')
        
        if role != 'parent':
            if not email:
                raise serializers.ValidationError("email:" "email is for this role necessary ")
        return attrs
    
    
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
    
    def validate_role(self, value):
        valid_roles = dict(User.Roles.choices).keys()
        print(valid_roles)
        if not value:
             raise serializers.ValidationError("User type is required.")
        if value not in valid_roles:
                raise serializers.ValidationError("Invalid user type.")
        return value
    
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        username = self.validated_data['username']
        email = self.validated_data['email']
        role = self.validated_data['role']
        children_data = validated_data.pop('children', [])
        
        if len(children_data) < 0:
                raise serializers.ValidationError("Only parents can have children.")

        user = User(
            username=username,
            email=email,
            role=role
            )
        user.set_password(password)
        user.save()
        for child_data in children_data:
            token = generate_random_token()
            child_data['password'] = token
            Child.objects.create(parent=user,**child_data)
        return user



User = get_user_model()
class LoginParentSerializer(TokenObtainPairSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()                     
   
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {

             'password': {'write_only': True},  'email': {'required': True}
        }
        
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
            
    def validate(self, attrs):
        print(attrs)
        email = attrs.get('email')
        password= attrs.get('password')
        user = User.objects.filter(email=email).first()
        
    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
        
        if user.role != 'parent':
            raise serializers.ValidationError("User type is not parent.")
        
        
        if not user.check_password(password.strip()):
            raise serializers.ValidationError("wrong password")

        data = super().validate({"username": user.username, "password": password, "role": user.role})
    
        
        return data
    

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

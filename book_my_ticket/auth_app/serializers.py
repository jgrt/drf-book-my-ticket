from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth', 'city', 'is_staff']


class UserLoginSerializer(serializers.Serializer):
    '''
    TODO validate
    '''
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    city = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.date_of_birth = self.validated_data.get('date_of_birth', '')
        user.city = self.validated_data.get('city', '')
        user.save(update_fields=['first_name', 'last_name', 'date_of_birth', "city"])

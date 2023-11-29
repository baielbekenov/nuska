from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from apps.authentication.models import Soglashenie
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": _("Неправильный логин или пароль")
    }


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=False)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password1 = serializers.CharField()
    email = serializers.EmailField()
    agreement_accepted = serializers.BooleanField(default=False)
    
    class Meta:
        model = User
        fields = ("phone", "password1", 'email', 'first_name', 'last_name', 'agreement_accepted')
        

    def validate_password1(self, password1):
        if not validate_password(password1):
            return password1
        
    
    def validate_agreement_accepted(self, value):
        if not value:
            raise serializers.ValidationError("Каттоодон өтүү үчүн келишимдин шарттарын кабыл алышыңыз керек.")

    
        
    
    


class UserGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "username",
            "groups",
            "user_permissions",
            "code",
        )


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': ('Токен эскирди же туура эмес')
    }
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
    

class SoglashenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soglashenie
        fields = '__all__'
        
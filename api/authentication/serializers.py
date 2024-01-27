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
        "no_active_account": _("Туура эмес логин же сырсөз")
    }


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=False)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password1 = serializers.CharField()
    email = serializers.EmailField()
    
    class Meta:
        model = User
        fields = ("phone", "password1", 'email', 'first_name', 'last_name')


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


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Почта жок!")
        return value
    
    
class CodeResetPasswordSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    email = serializers.EmailField()
    
    def validate_code(self, value):
        if len(str(value)) != 6 or value < 0:
            raise serializers.ValidationError('Код алты сандан турушу керек!')
        return value
    

class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    
    def validate_new_password(self, new_password):
        if not validate_password(new_password):
            return new_password


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']

        
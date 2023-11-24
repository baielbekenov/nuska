from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from apps.authentication.models import Soglashenie
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

    def validate_password1(self, password1):
        if not validate_password(password1):
            return password1

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


class SoglashenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soglashenie
        fields = '__all__'
        
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import password_validation
from django.conf import settings

User = get_user_model()


class UserAccountSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return request.build_absolute_uri(obj.avatar.url)
        return None

    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'first_name', 'last_name', 'patronymic',
                  'avatar', 'is_confirm']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен.")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value, self.context['request'].user)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
from django.conf import settings
from rest_framework import serializers
from .models import User, Soglashenie, Author, Jenre, Izdatel, Customer, Book, Order, Postuplenie, Comment


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser']
        ref_name = 'ProjectUserSerializer'

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username already exists', code='409')
        return value

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        user = User.objects.create(username=validated_data['username'],
                                   first_name=first_name,
                                   last_name=last_name, email=email)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
        
    
class SoglashenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soglashenie
        fields = '__all__'
        

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
        
class IzdatelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izdatel
        fields = '__all__'
        
        
class JenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jenre
        fields = '__all__'
        
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
class PostuplenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postuplenie
        fields = '__all__'
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
    
    
from rest_framework import serializers
from apps.library.models import Author, Izdatel, Jenre, Book, Comment


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
        

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
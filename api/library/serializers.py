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
        

class BookDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id','name', 'author', 'jenre', 'description', 'avatar',
                  'short_book_file', 'book_file', 'book_file', 
                  'izdatel', 'year_izdat', 'amount_pages', 'rating',
                  'cover_image', 'comments']
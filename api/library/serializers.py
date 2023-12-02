from rest_framework import serializers
from apps.library.models import Author, Jenre, Book, Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
        
class JenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jenre
        fields = '__all__'
        

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'
        

class BookListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'created_at', 'cover_image', 'jenre']
        

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
                  'amount_pages', 'created_at', 'sales_count',
                  'cover_image', 'comments']


class BestSellingBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'sales_count', 'jenre', 'cover_image']


class NewBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'created_at', 'jenre', 'cover_image' ]
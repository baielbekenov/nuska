from rest_framework import serializers
from apps.library.models import Author, Jenre, Book, Comment, FavoriteBook
from apps.authentication.models import User


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


class AddFavoriteBookSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = FavoriteBook
        fields = ['id', 'user', 'book', 'added_on']

    def create(self, validated_data):
        favorite_book, created = FavoriteBook.objects.get_or_create(**validated_data)
        return favorite_book


class ListFavoriteBookSerializer(serializers.Serializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = FavoriteBook
        fields = ['id', 'book']

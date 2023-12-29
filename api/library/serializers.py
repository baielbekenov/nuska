from rest_framework import serializers

from api.orders.serializers import PostuplenieSerializer
from apps.library.models import Author, Jenre, Book, Comment, FavoriteBook


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
        
class JenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jenre
        fields = '__all__'
        

class BookSerializer(serializers.ModelSerializer):
    prices = PostuplenieSerializer(many=True, read_only=True, source='postu_book')
    author = AuthorSerializer(many=True, read_only=True)
    jenre = JenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'created_at', 'cover_image', 'jenre', 'prices', 'sales_count']


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user_id.phone', read_only=True)

    class Meta:
        model = Comment
        fields = ['user_name', 'date', 'comment']
        

class BookDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id','name', 'author', 'jenre', 'description', 'avatar',
                  'short_book_file', 'book_file', 'amount_pages',
                  'created_at', 'sales_count',
                  'cover_image', 'comments']


class AddFavoriteBookSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = FavoriteBook
        fields = ['id', 'user', 'book', 'added_on']

    def create(self, validated_data):
        favorite_book, created = FavoriteBook.objects.get_or_create(**validated_data)
        return favorite_book


class ListFavoriteBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = FavoriteBook
        fields = ['id', 'book', 'added_on']

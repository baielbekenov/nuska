from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.orders.models import Order, Postuplenie, PublicOffer, Payment
from apps.library.models import Book, Jenre, Author


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['book']

    # def validate_book(self, value):
    #     try:
    #         # Пытаемся получить книгу по ID
    #         Book.objects.get(id=value)
    #     except ObjectDoesNotExist:
    #         # Если книги с таким ID не существует, генерируем ошибку валидации
    #         raise serializers.ValidationError("Book with this ID does not exist.")
    #     return value


class JenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jenre
        fields = ['name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']


class BookSerializer(serializers.ModelSerializer):
    jenre = JenreSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'cover_image', 'jenre']


class OrderSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Order
        fields = ['id', 'book', 'order_date', 'order_status']


class BookDetailSerializer(serializers.ModelSerializer):
    jenre = JenreSerializer(many=True, read_only=True)
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['name', 'author', 'cover_image', 'jenre',
                  'description', 'book_file', 'amount_pages', 'cover_image']


class OrderDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'book', 'order_date', 'order_status']



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'amount', 'payment_date', 'status', 'transaction_id']
        read_only_fields = ['payment_date', 'status', 'transaction_id']


class PostuplenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postuplenie
        fields = ['price']


class PublicOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicOffer
        fields = ['id', 'title', 'content', 'is_active']

        
        
from rest_framework import serializers
from apps.orders.models import Order, Postuplenie, PublicOffer


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id_book', ]


class BookSerializer


class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'id_user', 'id_book']


class PostuplenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postuplenie
        fields = ['price']


class PublicOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicOffer
        fields = ['id', 'title', 'content', 'is_active']

        
        
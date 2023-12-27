from rest_framework import serializers
from apps.orders.models import Order, Postuplenie, PublicOffer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class PostuplenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postuplenie
        fields = ['price']


class PublicOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicOffer
        fields = ['id', 'title', 'content', 'is_active']

        
        
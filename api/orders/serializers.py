from rest_framework import serializers
from apps.orders.models import Order, Postuplenie, PublicOffer, Payment


class OrderCreateSerializer(serializers.ModelSerializer):
    total_sum = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['book', 'total_sum']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'book', 'total_sum', 'order_date', 'order_status']
        read_only_fields = ['user', 'order_date', 'order_status']


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

        
        
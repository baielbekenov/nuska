from rest_framework import serializers
from apps.orders.models import Order, Postuplenie


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class PostuplenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postuplenie
        fields = '__all__'
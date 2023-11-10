from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from apps.orders.models import Order, Postuplenie
from api.orders.serializers import OrderSerializer, PostuplenieSerializer



class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class PostuplenieListView(generics.ListAPIView):
    queryset = Postuplenie.objects.all()
    serializer_class = PostuplenieSerializer
    


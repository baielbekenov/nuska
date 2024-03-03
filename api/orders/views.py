from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from apps.library.models import Book
from apps.orders.models import Order, Postuplenie, PublicOffer, Payment, Banner
from api.orders.serializers import PostuplenieSerializer, PublicOfferSerializer, OrderSerializer, PaymentSerializer, \
    OrderCreateSerializer, OrderDetailSerializer, BannerSerializer


class PurchaseBookView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "туура эмес жооп"}, status=status.HTTP_400_BAD_REQUEST)
        book_id = serializer.validated_data["book"]
        book = get_object_or_404(Book, name=book_id)

        Order.objects.create(
            user=request.user,
            book=book,
            total_sum=book.price
        )

        return Response({"message": "Заказ создан"}, status.HTTP_201_CREATED)


class PurchasedBookView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.filter(user=request.user, order_status=True)
        serializer = self.serializer_class(order, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailPurchasedBookView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class PostuplenieListView(generics.ListAPIView):
    queryset = Postuplenie.objects.all()
    serializer_class = PostuplenieSerializer


class PublicOfferView(generics.ListAPIView):
    queryset = PublicOffer.objects.all()
    serializer_class = PublicOfferSerializer
    permission_classes = (AllowAny,)


class BannerView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = (AllowAny, )

    


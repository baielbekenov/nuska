from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from apps.orders.models import Order, Postuplenie, PublicOffer
from api.orders.serializers import OrderCreateSerializer, PostuplenieSerializer, PublicOfferSerializer, \
    OrderListSerializer


class OrderUserListView(APIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.filter(id_user=self.request.user)
        serializer = self.serializer_class(order, many=True, context={'request': request})
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        order = serializer.save(id_user=self.request.user)
        book = order.id_book

        if book:
            postuplenie = Postuplenie.objects.filter(id_book=book).first()
            if postuplenie:
                print('price: ', postuplenie.price)
                order.totall_summ = postuplenie.price
            book.sales_count += 1
            book.save()
        order.save()

    def create(self, request, *args, **kwargs):
        # Обработка запроса на создание заказа
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Возврат успешного ответа с данными созданного заказа
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostuplenieListView(generics.ListAPIView):
    queryset = Postuplenie.objects.all()
    serializer_class = PostuplenieSerializer


class PublicOfferView(generics.ListAPIView):
    queryset = PublicOffer.objects.all()
    serializer_class = PublicOfferSerializer
    permission_classes = (AllowAny,)
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from apps.library.models import Book
from apps.orders.models import Order, Postuplenie, PublicOffer, Payment
from api.orders.serializers import PostuplenieSerializer, PublicOfferSerializer, OrderSerializer, PaymentSerializer


class PurchaseBookView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        user = request.user
        book_id = request.data.get('book_id')

        try:
            book = Book.objects.get(id=book_id)
            postuplenie = Postuplenie.objects.filter(book=book).order_by('-date').first()

            if not postuplenie:
                return Response({'error': 'Цена книги не найдена'}, status=status.HTTP_404_NOT_FOUND)

            # Создание заказа
            order_data = {'user': user.id, 'book': book_id, 'total_sum': postuplenie.price}
            order_serializer = OrderSerializer(data=order_data)
            order_serializer.is_valid(raise_exception=True)
            order = order_serializer.save()

            # Создание платежа
            payment_data = {'order': order.id, 'amount': postuplenie.price}
            payment_serializer = PaymentSerializer(data=payment_data)
            payment_serializer.is_valid(raise_exception=True)
            payment_serializer.save()

            return Response({'message': 'Книга успешно куплена'}, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)



class PostuplenieListView(generics.ListAPIView):
    queryset = Postuplenie.objects.all()
    serializer_class = PostuplenieSerializer


class PublicOfferView(generics.ListAPIView):
    queryset = PublicOffer.objects.all()
    serializer_class = PublicOfferSerializer
    permission_classes = (AllowAny,)
    


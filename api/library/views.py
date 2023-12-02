from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from api.library.pagination import CommentPagination
from apps.library.models import Author, Jenre, Book, Comment
from api.library.serializers import AuthorSerializer, BookListSerializer, JenreSerializer, \
    BookSerializer, CommentSerializer, BookDetailSerializer, BestSellingBookSerializer, NewBookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
    
from rest_framework.permissions import AllowAny, IsAuthenticated


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Comment.objects.filter(book_id=book_id)

    def post(self, request, *args, **kwargs):
        book_id = self.kwargs['book_id']
        book = get_object_or_404(Book, pk=book_id)  # Retrieve the Book instance

        # Получите данные для комментария из запроса
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраните комментарий с указанным book_id
            serializer.save(book_id=book, user_id=request.user)  # Assign the Book instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

class JenreListView(generics.ListAPIView):
    queryset = Jenre.objects.all()
    serializer_class = JenreSerializer
    
    
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        queryset = Book.objects.filter(active=True)
        jenre_id = self.request.query_params.get('jenre_id', None)

        if jenre_id is not None:
            queryset = queryset.filter(jenre__id=jenre_id)
        return queryset
    

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = [JWTAuthentication]


class BestSellingBooksView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-sales_count')
    serializer_class = BestSellingBookSerializer
    permission_classes = (AllowAny,)


class NewBooksView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = NewBookSerializer
    permission_classes = (AllowAny,)
    
    


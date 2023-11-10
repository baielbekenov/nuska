from rest_framework import status, generics
from apps.library.models import Author, Jenre, Izdatel, Book, Comment
from api.library.serializers import AuthorSerializer, JenreSerializer, IzdatelSerializer, \
    BookSerializer, CommentSerializer


    

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

class JenreListView(generics.ListAPIView):
    queryset = Jenre.objects.all()
    serializer_class = JenreSerializer
    

class IzdatelListView(generics.ListAPIView):
    queryset = Izdatel.objects.all()
    serializer_class = IzdatelSerializer
    
    
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    
    def get_object(self):
        # Опционально: переопределите этот метод, если нужно особое поведение при получении объекта
        return super().get_object()
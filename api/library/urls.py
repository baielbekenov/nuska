from django.urls import path
from api.library import views


urlpatterns = [
    path('author_list/', views.AuthorListView.as_view()),
    path('jenre_list/', views.JenreListView.as_view()),
    path('book_list/', views.BookListView.as_view()),
    path('comment_list_create/<int:book_id>/', views.CommentListAPIView.as_view()),
    
    path('book_detail/<int:pk>/', views.BookDetailView.as_view()),
    path('bestselling_books/', views.BestSellingBooksView.as_view()),
    path('newbooks/', views.NewBooksView.as_view()),
    path('recommended/books', views.RecommendedBooksView.as_view()),

    path('addfavoritebook/', views.AddFavoriteBookView.as_view()),
    path('deletefavoritebook/<int:pk>', views.DeleteFavouriteBookView.as_view()),
    path('favoritebook-list/', views.ListFavoriteBookView.as_view())
    
    
]
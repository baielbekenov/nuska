from django.urls import path
from api.library import views


urlpatterns = [
    path('author_list/', views.AuthorListView.as_view()),
    path('jenre_list/', views.JenreListView.as_view()),
    path('izdatel_list/', views.IzdatelListView.as_view()),
    path('book_list/', views.BookListView.as_view()),
    path('comment_list/', views.CommentListView.as_view()),
    
    path('book_detail/<int:pk>/', views.BookDetailView.as_view()),
    
    
]
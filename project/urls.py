from django.urls import path
from project import views


urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    
    path('orderlist/', views.OrderListView.as_view()),
    path('user_list/', views.UserListView.as_view()),
    path('sogl_list/', views.SoglashenieListView.as_view()),
    path('author_list/', views.AuthorListView.as_view()),
    path('jenre_list/', views.JenreListView.as_view()),
    path('izdatel_list/', views.IzdatelListView.as_view()),
    path('customer_list/', views.CustomerListView.as_view()),
    path('book_list/', views.BookListView.as_view()),
    path('postuplenie_list/', views.PostuplenieListView.as_view()),
    path('comment_list/', views.CommentListView.as_view()),
    
    path('book_detail/<int:pk>/', views.BookDetailView.as_view()),
    
    
]
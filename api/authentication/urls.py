from django.urls import path
from api.authentication import views


urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    
    path('user_list/', views.UserListView.as_view()),
    path('sogl_list/', views.SoglashenieListView.as_view()),
    
    
    
]
from django.urls import path
from api.authentication import views


urlpatterns = [
    path("login/", views.CustomTokenObtainView.as_view(), name="token_obtain_pair"),
    path('register/', views.RegistrationAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    
    path('user_list/', views.UserListView.as_view()),
    path('sogl_list/', views.SoglashenieListView.as_view()),
    
    path('users/reset/password/', views.ResetPasswordView.as_view()),
    path('users/reset/code/confirm/', views.CodeResetPasswordView.as_view()),
    path('users/reset/password/confirm/', views.ResetPasswordConfirmView.as_view()),
    
    
    
]
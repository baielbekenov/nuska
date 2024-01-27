from django.urls import path
from api.authentication import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", views.CustomTokenObtainView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', views.RegistrationAPIView.as_view()),

    path('users/reset/password/', views.ResetPasswordView.as_view()),
    path('users/reset/code/confirm/', views.CodeResetPasswordView.as_view()),
    path('users/reset/password/confirm/', views.ResetPasswordConfirmView.as_view()),
    path('user/list/', views.UserListView.as_view()),
    
    
    
]
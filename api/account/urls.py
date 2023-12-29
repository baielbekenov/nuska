from django.urls import path
from api.account.views import UserAccountUpdateView, ChangePasswordView, ConfirmUserEmailView, \
    ActivateEmailUserView, SendCodeAgainView, GetMeApiView, UserDeleteView


urlpatterns = [
    path("user/update/", UserAccountUpdateView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("confirm/email/", ConfirmUserEmailView.as_view()),
    path("activate/email/", ActivateEmailUserView.as_view()),
    path("send/code/again/", SendCodeAgainView.as_view()),
    path("users/me/", GetMeApiView.as_view()),
    path('delete/account/<int:pk>/', UserDeleteView.as_view())
]
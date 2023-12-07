from django.urls import path
from api.account.views import UserAccountUpdateView, ChangePasswordView


urlpatterns = [
    path("user/update/", UserAccountUpdateView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
]
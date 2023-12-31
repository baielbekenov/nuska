from django.urls import path, include


urlpatterns = [
    path("account/", include("api.account.urls")),
    path("authentication/", include("api.authentication.urls")),
    path("library/", include("api.library.urls")),
    path("orders/", include("api.orders.urls")),
    path("docs/", include("api.openapi.urls")),
]
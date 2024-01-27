from django.urls import path
from api.orders import views


urlpatterns = [
    path('postuplenie_list', views.PostuplenieListView.as_view()),
    path('public_offer', views.PublicOfferView.as_view()),
    path('purchase/book', views.PurchaseBookView.as_view()),
    # path('order/user/list', views.OrderUserListView.as_view())
    
]
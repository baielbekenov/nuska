from django.urls import path
from api.orders import views


urlpatterns = [
    path('orderlist/', views.OrderListView.as_view()),
    path('postuplenie_list/', views.PostuplenieListView.as_view()),
    
    
]
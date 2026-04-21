from django.urls import path
from .views import PlaceOrderView

urlpatterns = [
    path('orders/place/', PlaceOrderView.as_view()),
]
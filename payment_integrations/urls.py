from django.urls import path
from .views import CheckoutView,PaymentProcessView,payment_success

urlpatterns = [
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('payment/',PaymentProcessView.as_view(),name='payment'),
    path("payment_success/", payment_success, name="payment_success"),
]
from django.urls import path
from .views import Home,FruitCollectionView,FruitDetailView,CartView,FruitIdView,CartProductUpdate,CartProductDelete,AboutView,ContactView,ContactUsAjax

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('shop/',FruitCollectionView.as_view(),name='shop'),
    path('fruit/',FruitIdView.as_view(),name='fruit'),
    path('shop/<int:pk>',FruitDetailView.as_view(),name='fruitdetail'),
    path('cart/',CartView.as_view(),name='cart'),
    path('cart-update/',CartProductUpdate.as_view(),name='cart-update'),
    path('cart-delete/',CartProductDelete.as_view(),name='cart-delete'),
    path('about/',AboutView.as_view(),name='about'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('contact_form/',ContactUsAjax.as_view(),name='contact_form'),
]
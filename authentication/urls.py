from django.urls import path
from .views import Login,UserRegister
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/',UserRegister.as_view(),name='signup')
]

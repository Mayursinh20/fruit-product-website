from django.contrib import admin
from .models import ProductDetail,Cart,CheckoutAddress

# Register your models here.
admin.site.register(ProductDetail)
admin.site.register(Cart)
admin.site.register(CheckoutAddress)

from django.db import models
from authentication.models import User

# Create your models here.
class ProductDetail(models.Model):
    name = models.CharField(max_length=225,null=True,blank=False)
    price = models.CharField(max_length=225,null=True,blank=False)
    description = models.TextField(null=True,blank=False)
    images = models.ImageField(upload_to='fruit/',null=True,blank=False)

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,null=True,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True,blank=False)
    total = models.CharField(max_length=225,null=True,blank=False)

    def __str__(self) -> str:
        return f"{self.user.username} --> {self.cart.name}"


class CheckoutAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=225,null=True,blank=False,verbose_name='First name')
    last_name = models.CharField(max_length=225,null=True,blank=False,verbose_name='Last name')
    contact = models.CharField(max_length=11,null=True,blank=False,verbose_name="Contact no")
    email = models.CharField(max_length=225,null=True,blank=False,verbose_name="Email address")
    address = models.CharField(max_length=225,null=True,blank=False,verbose_name='User address')
    country = models.CharField(max_length=225, null=True, blank=True) 
    city = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225,null=True,blank=False,verbose_name="state name")
    zip_code = models.CharField(max_length=10,null=True,blank=False,verbose_name="Zip code")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

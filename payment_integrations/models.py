from django.db import models
from authentication.models import User

# Create your models here.
class Payment(models.Model):
    Payment_Status = (
        ("SUCCESS","success"),
        ("FAILURE","failure"),
        ("PENDING","pending")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="pg_razorpay_user",verbose_name="User of Razorpay",help_text="User of Razorpay")
    status = models.CharField(max_length=100,choices=Payment_Status,null=True,blank=False)
    amount = models.CharField(max_length=225,null=True,blank=False)
    razorpay_payment_id = models.CharField(max_length=255,null=True,blank=True,unique=True,verbose_name="Razorpay payment id",help_text="Razorpay payment id")
    razorpay_order_id = models.CharField(max_length=255,verbose_name="Razorpay order id",help_text="Razorpay order id")
    razorpay_signature = models.CharField(max_length=255,null=True,blank=True,verbose_name="Razorpay signature",help_text="Razorpay signature")

    def __str__(self):
        return f"""User: {self.user} | Order Id: {self.razorpay_order_id} | Payment Id: {self.razorpay_payment_id}"""

    class Meta:
        db_table = "razorpay_details"
        verbose_name = "Razorpay Payment Detail"
        verbose_name_plural = "Razorpay Payment Details"
from django.db import models
from authentication.models import User
# Create your models here.
class ContactUs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=225,null=True,blank=False,verbose_name="Name",help_text="Enter name")
    email = models.EmailField(max_length=225,null=True,blank=False,verbose_name="Email",help_text="Enter email")
    phone = models.CharField(max_length=225,null=True,blank=False,verbose_name="Contact no",help_text="Contact no")
    subject = models.CharField(max_length=225,null=True,blank=False,verbose_name="Subject",help_text="Customer queries")
    message = models.TextField(max_length=225,null=True,blank=False,verbose_name="Message",help_text="Enter message")

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
from django import forms
from .models import CheckoutAddress
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class CheckoutForm(forms.ModelForm):
    first_name = forms.CharField(error_messages={'required':'Enter first name'})
    last_name = forms.CharField(error_messages={'required':'Enter last name'})
    contact = forms.CharField(validators=[validators.MaxLengthValidator(10), validators.MinLengthValidator(10)],error_messages={'required':'Enter contact number'})
    email = forms.CharField(error_messages={'required':'Enter email address'},validators=[RegexValidator('([A-Za-z]+[.-_])*[A-Za-z]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')])
    address = forms.CharField(error_messages={'required':'Enter address'},widget=forms.Textarea)
    country = forms.CharField(error_messages={'required':'Enter address'},widget=forms.Textarea)
    city = forms.CharField(error_messages={'required':'Enter address'},widget=forms.Textarea)
    state = forms.CharField(error_messages={'required':'Enter state'})
    zip_code = forms.CharField(error_messages={'required':'Enter zip code'})

    class Meta:
        model = CheckoutAddress
        fields = ['first_name','last_name','contact','email','address','country','city','state','zip_code']
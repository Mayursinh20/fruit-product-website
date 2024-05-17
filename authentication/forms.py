from django import forms
from .models import User

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(error_messages={'required':'Enter email id'})
    username = forms.CharField(error_messages={'required':'Enter username'},required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

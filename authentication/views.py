from django.shortcuts import render,redirect
from django.views.generic import View,CreateView
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .forms import UserRegisterForm
from django.urls import reverse_lazy

# Create your views here.
class Login(View):

    def get(self, request):
        """
        Get method called if user is authenticated it automatically redirect
        to users page
        """
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, "authentication/login.html")

    def post(self, request):
        """
        Post method called
        """
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                    
                else:
                    messages.error(request, "User Does not exist")
                    return redirect('login')
            else:
                messages.error(
                    request, "Please enter valid email and Password")
                return redirect('login')
        else:
            messages.error(request, "Please enter email and Password")
            return redirect('login')
        

class UserRegister(CreateView):
    """
    New user create
    """
    form_class = UserRegisterForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')
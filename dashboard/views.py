from typing import Any
from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView,View,CreateView
from product.models import ProductDetail,Cart
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ContactUs

# Create your views here.

class Home(ListView):
    """
    List of product
    Return: Product list
    """
    model = ProductDetail
    template_name = 'dashboard/home.html'
    context_object_name = 'fruitdetail'

class FruitCollectionView(TemplateView):
    """"
    Collection of fruit
    """
    template_name = 'product/fruit-collection.html'

    def get_context_data(self, **kwargs):
        """
        Return : All product details as context
        """
        context = super().get_context_data(**kwargs)
        context['fruitdetail'] = ProductDetail.objects.all()
        return context

class FruitIdView(LoginRequiredMixin,View):
    """
    Create or Update cart as fruit id
    post : Return create or update cart and total quantity
    get_product_details : Return the product
    update_or_create_cart_entry : Return update or create cart with count
    """

    def post(self, request):
        """
        Return : Jsonrepsonse that total quantity and product create or update
        """
        try:
            fruit_id = request.POST.get("fruit_id")
            product = self.get_product_details(fruit_id)
            if product:
                cart = self.update_or_create_cart_entry(product)
                quantity = Cart.objects.filter(user=self.request.user).aggregate(quantity=Sum('quantity'))['quantity']
                return JsonResponse({"id": fruit_id,"quantity":quantity})
            else:
                return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get_product_details(self, fruit_id):
        """
        Return : Particular product as filter
        """
        product = ProductDetail.objects.filter(id=fruit_id).values('name', 'price').first()
        return product

    def update_or_create_cart_entry(self, product):
        """"
        Return : create or update cart and plus quantity and total increase
        """
        price = product['price']
        product_detail = get_object_or_404(ProductDetail, name=product['name'])
        cart, created = Cart.objects.get_or_create(user=self.request.user,cart=product_detail, defaults={'quantity': 1, 'total': price})
        if not created:
            cart.quantity += 1
            cart.total = int(price) * cart.quantity
            cart.save()


class FruitDetailView(LoginRequiredMixin,DetailView):
    """
    Return : Particular Product list
    """
    model = ProductDetail
    template_name = 'product/fruit-details.html'
    context_object_name = 'fruitdata'

    def get_context_data(self, *args,**kwargs):
        context = super(FruitDetailView,self).get_context_data(*args,**kwargs)
        context['fruitdetails'] = ProductDetail.objects.all()
        return context
    
class CartView(LoginRequiredMixin,TemplateView):
    """
    Return : Total cart as per user and subtotal
    """
    template_name = 'product/cart.html'

    def get_context_data(self,*args,**kwargs):
        context = super(CartView,self).get_context_data(*args,**kwargs)
        context['cartdata'] = Cart.objects.filter(user=self.request.user)
        context['subtotal'] = Cart.objects.filter(user=self.request.user).aggregate(subtotal=Sum('total'))['subtotal']
        return context
    
class CartProductUpdate(LoginRequiredMixin,View):
    """
    Return : Increase or decrease product
    """

    def post(Self,request):
        """
        Return : Jsonresponse that increase or decrease product count
        """
        cart_id = request.POST.get("cart_id")
        total = request.POST.get("total")
        quantity = request.POST.get("quantity")
        cart = Cart.objects.filter(user=request.user,id=cart_id).update(quantity=quantity,total=total)
        quantity = Cart.objects.filter(user=request.user).aggregate(quantity=Sum('quantity'))['quantity']
        return JsonResponse({"msg":"success","quantity":quantity})
    
class CartProductDelete(LoginRequiredMixin,View):
    """
    Return : Remove the product in datatable
    """

    def post(self,request):
        cart_id = request.POST.get("cart_id")
        cart = Cart.objects.filter(user=request.user,id=cart_id).delete()
        quantity = Cart.objects.filter(user=self.request.user).aggregate(quantity=Sum('quantity'))['quantity']
        return JsonResponse({"msg":"delete","quantity":quantity})

class AboutView(LoginRequiredMixin,TemplateView):
    """
    About page
    """
    template_name = "dashboard/about.html"
    

class ContactView(LoginRequiredMixin,TemplateView):
    """
    Contact page
    """
    template_name = 'dashboard/contact.html'

    def get_context_data(self,*args, **kwargs: Any) -> dict[str, Any]:
        context = super(ContactView,self).get_context_data(*args,**kwargs)
        context['contact-us'] = ContactUs.objects.all()
        return context

class ContactUsAjax(LoginRequiredMixin,View):
    """"
    Return : Jsonreposne
    create customer queries
    """

    def post(self,request):
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        phone = self.request.POST.get('phone')
        subject = self.request.POST.get('subject')
        message = self.request.POST.get('message')
        # import pdb;pdb.set_trace()
        if name != '' and email != '' and phone != '' and subject != '' and message != '':
            contact_us = ContactUs.objects.create(user=self.request.user,name=name,email=email,phone=phone,subject=subject,message=message)
            return JsonResponse({"msg":"Your application submitted"},status=200)
        else:
            return JsonResponse({"msg":"error",})

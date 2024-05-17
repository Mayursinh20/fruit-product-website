from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,CreateView
from product.forms import CheckoutForm
from product.models import Cart
from django.db.models import Sum
import razorpay
from razorpay import errors
from django.conf import settings
from .models import Payment
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseBadRequest,JsonResponse

# Create your views here.
class CheckoutView(CreateView):
    form_class = CheckoutForm
    template_name = "payment/checkout.html"

    def get_context_data(self,*args,**kwargs):
        context = super(CheckoutView,self).get_context_data(*args,**kwargs)
        subtotal = Cart.objects.filter(user=self.request.user).aggregate(subtotal=Sum('total'))['subtotal']
        context["product_data"] = Cart.objects.filter(user=self.request.user).values('cart__name','total')
        context['subtotal'] = subtotal
        context['total'] = subtotal
        return context

class PaymentProcessView(View):
    
    def post(self,request,*args):
        subtotal = Cart.objects.filter(user=self.request.user).aggregate(subtotal=Sum('total'))['subtotal']
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(subtotal) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Payment.objects.create(user=request.user,amount=subtotal, razorpay_order_id=razorpay_order["id"])
        return render(request,"payment/payment.html",{
                "callback_url": "http://" + "127.0.0.1:8000" + "/frutika/payment_success/",
                "razorpay_key": settings.RAZOR_KEY_ID,
                "order": order,
                "amount":int(subtotal) * 100
            },
        )
@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': signature
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            payment_success = Payment.objects.get(razorpay_order_id=order_id)
            payment_success.razorpay_payment_id = razorpay_payment_id
            payment_success.razorpay_signature = signature
            payment_success.status = "SUCCESS"
            payment_success.save()

            return render(request, 'payment/payment_success.html')
        except Exception as e:
            return HttpResponseBadRequest("Payment verification failed")
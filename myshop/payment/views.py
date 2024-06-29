from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render , reverse, redirect, get_object_or_404
from orders.model import Order
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION



def payment_process(request):
    order_id = request.session.get('order_id',None)
    order = get_object_or_404(Order,id=order_id)
    
    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        
    else:
        return render(
            request,
            'payment/process.html',
            locals()
        )
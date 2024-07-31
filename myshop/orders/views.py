from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse
from .models import OrderItem , Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
#import weasyprint
from xhtml2pdf import pisa
import os
import io

# Create your views here.

# creating the order view for the end  user
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()

            # launch asynchronous task
            order_created.delay(order.id)
            # set the order for the session
            request.session['order_id'] =  order.id
            # redirect for the payment
            return redirect(reverse('payment:process')) 
            
        
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {
            'cart':cart,
            'form': form
        }
    )
    
    
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        'admin/orders/order/detail.html',
        {
            'order' : order
        }
    )


@staff_member_required
def admin_order_pdf(request,order_id):
    order = get_object_or_404(Order,id = order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    #weasyprint.HTML(string=html).write_pdf(response,
    #stylesheets=[weasyprint.CSS(
        #settings.STATIC_ROOT / 'css/pdf.css')])
    result = io.BytesIO()
    pdf = pisa.CreatePDF(
        src=html,
        dest=result,
        link_callback=fetch_resources,
        default_css=css
    )
    
    if pdf.err:
        return HttpResponse('We had some errors with the PDF generation')

    response.write(result.getvalue())
    return response


def fetch_resources(uri, rel):
    path = os.path.join(settings.STATIC_ROOT,
                        uri.replace(settings.STATIC_URL, ""))
    return path

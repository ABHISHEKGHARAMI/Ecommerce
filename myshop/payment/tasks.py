from io import BytesIO
from celery import shared_task
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    
    subject = f"Tea shop - order : {order.id}"
    
    message = 'Please find the attachment with the invoice.'
    
    # setting the email
    email = EmailMessage(subject,
                         message,
                         'abhishekgharami1998@gmail.com',
                         [order.email])
    # generate the pdf for the invoice
    html = render_to_string('orders/order/pdf.html',
                            {'order':order})
    
    out = BytesIO()
    
    # creating the pdf using the xhtml2pdf
    
    pisa_status = pisa.CreatePDF(
        html,
        dest=out,
        link_callback = lambda uri,rel : f'setting.STATIC_ROOT/{uri}'
    )
    
    if pisa_status.err:
        return False
    
    # attach the css for style
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    
    # sending the email
    email.send()
    

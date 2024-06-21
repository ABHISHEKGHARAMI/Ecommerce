# setting up with the sessions

from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self,request):
        self.session = request.session
        
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            cart = self.session[settings.CART_SESSION_ID]
        self.cart = cart
        
    #adding the product for the cart
    def add(self,product,quantity=1,override_quality=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity' : 0,
                'price' : str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity 
            
        self.save()
    #save the modification
    def save(self):
        self.session.modified = True
        
    
    # remove from the cart
    def remove(self,product):
        product_id = str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()
        
        
        
    # iterate over the database for get the data for product
    def __iter__(self):
        pass
        
        
    
        
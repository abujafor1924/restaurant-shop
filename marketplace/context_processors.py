from .models import Cart
from menu.models import FoodItem
from vendor.models import Vendor

def get_cart_counter(request):   
    cart_count = 0 
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items.exists():
                for cart_item in cart_items:       
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        cart_count = 0

    return dict(cart_count=cart_count)

def get_cart_amount(request):   
    subtotal = 0
    tax=0
    grand_total=0
    
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items.exists():
                for cart_item in cart_items:    
                    fooditem = FoodItem.objects.get(id=cart_item.fooditem.id)   
                    subtotal += (fooditem.price * cart_item.quantity)
                    tax = (2 * subtotal)/100
                    grand_total = subtotal + tax
                    print(grand_total)
            else:
                subtotal = 0
        except Cart.DoesNotExist:
            subtotal = 0
    else:
        subtotal = 0
    
    return dict(subtotal=subtotal,tax=tax,grand_total=grand_total)
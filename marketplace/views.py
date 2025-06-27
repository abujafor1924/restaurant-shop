from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpResponse
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from .models import Cart
from marketplace.context_processors import get_cart_counter,get_cart_amount
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

# Create your views here.
def marketplace(request):
     vendor=Vendor.objects.filter(is_approved=True,user__is_active=True)
     vendor_count=vendor.count()
     context={
          'vendor':vendor,
          'vendor_count':vendor_count,
     }
     return render(request, 'marketplace/listing.html',context)

def vendor_details(request,vendor_slug):
     vendor=get_object_or_404(Vendor,vendor_slug=vendor_slug)
     categories=Category.objects.filter(vendor=vendor).prefetch_related(
          Prefetch('fooditems',queryset=FoodItem.objects.filter(is_available=True))
     )
     
     if request.user.is_authenticated:
          cart_items=Cart.objects.filter(user=request.user)
     else:     
            cart_items=None
     context={
          'vendor':vendor,
          'categories':categories,
          'cart_items':cart_items
     }     
     
     
     return render(request, 'marketplace/vendor_details.html',context)



def add_to_cart(request, food_id):     
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                fooditem = FoodItem.objects.get(id=food_id)

                cart, created = Cart.objects.get_or_create(
                    user=request.user,
                    fooditem=fooditem,
                    defaults={'quantity': 1}
                )

                if not created:
                    cart.quantity += 1
                    cart.save()
                    message = 'Product quantity updated in cart'
                else:
                    message = 'Product added to cart'

                return JsonResponse({'status': 'Success', 'message': message, 'cart_count': get_cart_counter(request),'qty':cart.quantity,'cart_amount':get_cart_amount(request)})

            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'Product does not exist'})
        else:
            return JsonResponse({'status': 'login required', 'message': 'Please login to continue'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    
    
def decrease_cart(request, food_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()
                    message = 'Product quantity updated in cart'
                else:
                    cart.delete()
                    cart.quantity = 0
                    message = 'Product removed from cart'

                return JsonResponse({'status': 'Success', 'message': message, 'cart_count': get_cart_counter(request),'qty':cart.quantity,'cart_amount':get_cart_amount(request)})
            except Cart.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'Product does not exist in cart'})
        else:
            return JsonResponse({'status': 'login required', 'message': 'Please login to continue'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Invalid request'}) 
    
@login_required(login_url='login')
def cart(request):
     cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
     context={
          'cart_items':cart_items
     }
     return render(request, 'marketplace/cart.html',context)
 
@login_required(login_url='login')
def delete_cart(request,cart_id):
     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
          if request.user.is_authenticated:
               try:
                    cart_item=Cart.objects.get(user=request.user,id=cart_id)
                    if cart_item:
                         cart_item.delete()
                         return JsonResponse({'status':'Success','message':'Product removed from cart','cart_count':get_cart_counter(request),'cart_amount':get_cart_amount(request)})
               except Cart.DoesNotExist:
                    return JsonResponse({'status':'Failed','message':'Product does not exist in cart'}) 
          else:
               return JsonResponse({'status':'login required','message':'Please login to continue'})    
     else:
          return JsonResponse({'status':'Failed','message':'Invalid request'})  


def search(request):
    keyword = request.GET['keyword']  
    address = request.GET['address']     
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    
    fetch_vendor_food_items=FoodItem.objects.filter(food_title__icontains=keyword,is_available=True).values_list('vendor',flat=True)
    print(fetch_vendor_food_items)
    vendor=Vendor.objects.filter(Q(id__in=fetch_vendor_food_items)|Q(vendor_name__icontains=keyword ),is_approved=True,user__is_active=True)    
    if latitude and longitude and radius:
        pnt=GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
        vendor = Vendor.objects.filter(
        (
            Q(id__in=fetch_vendor_food_items) |
            Q(vendor_name__icontains=keyword)
        ) &
        Q(is_approved=True) &
        Q(user__is_active=True) &
        Q(user_profile__location__distance_lte=(pnt, D(km=radius)))
        ).annotate(distance=Distance('user_profile__location', pnt)).order_by('distance')
        
    vendor_count = vendor.count()
    context = {
        'vendor': vendor,  # এটা QuerySet, মানে iterable — for loop করা যাবে
       
        'vendor_count': vendor_count
    }
   

    return render(request, 'marketplace/listing.html', context)



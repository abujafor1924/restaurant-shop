from django.shortcuts import render,get_object_or_404
from .forms import VendorForm
from accounts.forms import UserProfileForm
from .models import Vendor
from menu.models import Category
from accounts.models import UserProfile
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify

# Create your views here.

def get_vendor(request):      
     vendor=Vendor.objects.get(user=request.user) 
     return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
     profile=get_object_or_404(UserProfile,user=request.user)
     vendor=get_object_or_404(Vendor,user=request.user)
     
     if request.method=='POST':
          profile_form=UserProfileForm(request.POST, request.FILES, instance=profile)
          vendor_form=VendorForm(request.POST,request.FILES, instance=vendor) 
          
          if profile_form.is_valid() and vendor_form.is_valid():
               profile_form.save()
               vendor_form.save()
               messages.success(request,'Profile updated successfully')    
               return redirect('vprofile')
          else:
               print('invalid form')
               print(profile_form.errors)
     else:
          profile_form=UserProfileForm(instance=profile)
          vendor_form=VendorForm(instance=vendor)
     context={
          'profile_form':profile_form,
          'vendor_form':vendor_form,
          'profile':profile,
          'vendor':vendor,
     }
     
     return render(request, 'vendor/vprofile.html',context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
     vendor=get_vendor(request)
     categories=Category.objects.filter(vendor=vendor).order_by('category_name')
     context={
          'categories':categories     
     }
     
     return render(request, 'vendor/menu_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditem_by_category(request,pk=None):
     vendor=get_vendor(request)
     category=get_object_or_404(Category,pk=pk)
     fooditem=FoodItem.objects.filter(vendor=vendor,category=category)
     context={
          'fooditem':fooditem,
          'category':category
     }
     return render(request, 'vendor/fooditem_by_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
     if request.method=='POST':
          form=CategoryForm(request.POST)
          if form.is_valid():
               category_name=form.cleaned_data['category_name']
               category=form.save(commit=False)
               category.vendor=get_vendor(request)     
               category.slug=slugify(category_name)
               form.save()
               messages.success(request,'Category added successfully')
               return redirect('menu_builder')           
          else:
               print('invalid form')    
               print(form.errors)           
     else:
          form=CategoryForm() 
     context={
          'form'  : form,
     }
     return render(request, 'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def update_category(request,pk=None):
     category=get_object_or_404(Category,pk=pk)
     if request.method=='POST':
          form=CategoryForm(request.POST,instance=category)
          if form.is_valid():
               category_name=form.cleaned_data['category_name']
               category=form.save(commit=False)       
               category.slug=slugify(category_name)
               form.save()
               messages.success(request,'Category updated successfully')
               return redirect('menu_builder')           
          else:
               print('invalid form')    
               print(form.errors)           
     else:
          form=CategoryForm(instance=category) 
     context={
          'form'  : form,      
          'category':category
     }
   
     return render(request, 'vendor/update_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
     category=get_object_or_404(Category,pk=pk)
     category.delete()
     messages.success(request,'Category deleted successfully')
     return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_fooditem(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            fooditem = form.save(commit=False)
            fooditem.vendor = get_vendor(request)  # ভেন্ডর অ্যাসাইন করুন
            fooditem.slug = slugify(foodtitle)  # স্লাগ জেনারেট করুন
            fooditem.save()  # ফুড আইটেম সেভ করুন
            messages.success(request, 'FoodItem added successfully')
            return redirect('fooditem_by_category', pk=fooditem.category.id)  # রিডাইরেক্ট করুন
        else:
            print('invalid form')    
            print(form.errors)  # ফর্মের এরর দেখুন
    else:
        form = FoodItemForm()

    context = {
        'form': form,    
    }
    return render(request, 'vendor/add_fooditem.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def update_fooditem(request,pk=None):
    fooditem = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=fooditem)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            fooditem = form.save(commit=False)
            fooditem.vendor = get_vendor(request)  # ভেন্ডর অ্যাসাইন করুন
            fooditem.slug = slugify(foodtitle)  # স্লাগ জেনারেট করুন
            fooditem.save()  # ফুড আইটেম সেভ করুন
            messages.success(request, 'FoodItem updated successfully')
            return redirect('fooditem_by_category', pk=fooditem.category.id)  # রিডাইরেক্ট করুন
        else:
            print('invalid form')    
            print(form.errors)  # ফর্মের এরর দেখুন
    else:
        form = FoodItemForm(instance=fooditem)

    context = {
        'form': form,
        'fooditem': fooditem,
    }
    return render(request, 'vendor/update_fooditem.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_fooditem(request,pk=None):
    fooditem = get_object_or_404(FoodItem, pk=pk)
    fooditem.delete()
    messages.success(request, 'FoodItem deleted successfully')
    return redirect('fooditem_by_category', pk=fooditem.category.id)
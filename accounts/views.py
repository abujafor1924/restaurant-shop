from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import detectUserType, send_email_for_verification,send_test_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied



# Resticted user access
def check_role_vendor(user):
     if user.role == 1:
         return True
     else:
         return PermissionDenied

def check_role_customer(user):
     if user.role == 2:
         return True
     else:
         return PermissionDenied

# Create your views here.
def register(request):
     if request.user.is_authenticated:
          messages.warning(request,'You are already logged in')
          return redirect('myaccount')
     elif request.method=='POST':
       print(request.POST)
       form=UserForm(request.POST)
       if form.is_valid():
            password=form.cleaned_data['password']
            user=form.save(commit=False)
            user.role=User.CUSTOMER
            user.set_password(password)
            user.save()
            
            #email verification
            send_email_for_verification(request,user)
            send_test_email()
            
            messages.success(request,'Account created successfully')
            return redirect('home')
       else:
            print('invalid form')
            print(form.errors)
     else:
          form=UserForm()
          
     context={'form':form}
     
     return render(request, 'accounts/registerUser.html',context)

def registerVendor(request): 
     if request.user.is_authenticated:
          messages.warning(request,'You are already logged in')
          return redirect('myaccount')
     elif request.method=='POST':
          form=UserForm(request.POST)
          v_form=VendorForm(request.POST, request.FILES)
          if form.is_valid() and v_form.is_valid():
               user=form.save(commit=False)
               user.role=User.VENDOR
               user.save()
               vendor=v_form.save(commit=False)
               vendor.user=user
               user_profile=UserProfile.objects.get(user=user)
               vendor.user_profile=user_profile
               vendor.save()
               
               #email verification
               send_email_for_verification(request,user)
               send_test_email()
               
               messages.success(request,'Account created successfully, wait Approval from Admin')
               return redirect('home')
          else:
               print('invalid vendor form')
               print(form.errors)
               print(v_form.errors)
     else:
          form=UserForm()
          v_form=VendorForm()
     
     form = UserForm()
     v_form=VendorForm()
     
     context={
          'form':form,
          'v_form':v_form
     }
     
     return render(request, 'accounts/registerVendor.html', context)


def activate(request,uidb64,token):
   return

def login(request):
     if request.user.is_authenticated:
          messages.warning(request,'You are already logged in')
          return redirect('myaccount')
     elif request.method=='POST':
          email=request.POST['email']
          password=request.POST['password']  
          user=auth.authenticate(email=email, password=password)
          if user is not None:
               auth.login(request,user)
               messages.success(request,'You are now logged in')
               return redirect('home')  
          else:
               messages.error(request,'invalid credentials')           
               return redirect('login')
     return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('login')

@login_required(login_url='login')
def myaccount(request):
     user=request.user   
     redirectUrl=detectUserType(user)
     return redirect(redirectUrl)
     # return render(request, 'accounts/myaccount.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer )
def customerDashboard(request):
     return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
     return render(request, 'accounts/vendorDashboard.html')
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import detectUserType, send_email_for_verification,send_test_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from vendor.models import Vendor   
from django.utils.encoding import force_bytes
from django.template.defaultfilters import slugify





# Resticted user access
def check_role_vendor(user):
     if user.role == 1:
         return True
     return False
     # else:
     #     return PermissionDenied

def check_role_customer(user):
     if user.role == 2:
         return True
     return False
     # else:
     #     return PermissionDenied

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
            mail_subject='Please activate your account'
            email_template='accounts/email/account_verification_email.html'
            send_email_for_verification(request,user,mail_subject,email_template)
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
               vendor_name=v_form.cleaned_data['vendor_name']
               vendor.vendor_slug=slugify(vendor_name)+'-'+str(user.id)
               user_profile=UserProfile.objects.get(user=user)
               vendor.user_profile=user_profile
               vendor.save()
               
               #email verification
               mail_subject='Please activate your account'
               email_template='accounts/email/account_verification_email.html'
               send_email_for_verification(request,user,mail_subject,email_template)
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
   try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
   except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
   if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congrats! Your account is activated.')
        return redirect('login')
   else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

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
     vendor=Vendor.objects.get(user=request.user)
     contex={
          'vendor':vendor,
     }
     return render(request, 'accounts/vendorDashboard.html',contex)



def forgot_password(request):
     if request.method=='POST':
          email=request.POST['email']
          if User.objects.filter(email=email).exists():
               user=User.objects.get(email__exact=email)
               #send reset password email
               
               mail_subject='Reset your password'
               email_template='accounts/email/reset_password_email.html'
               
               send_email_for_verification(request,user,mail_subject,email_template)
               messages.success(request,'Password reset link has been sent to your email address')
               return redirect('login')
          else:
               messages.error(request,'Account does not exist')  
               return redirect('forgot_password')
     return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('set_new_password', uidb64=uidb64, token=token)

    else:
        messages.error(request, 'This link has been expired')
        return redirect('myaccount')

def set_new_password(request, uidb64, token):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match')
            return redirect('set_new_password', uidb64=uidb64, token=token)
    return render(request, 'accounts/set_new_password.html' , context={'uidb64':uidb64, 'token':token})
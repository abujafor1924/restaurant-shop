from django.urls import path,include
from . import views

urlpatterns = [
     path('', views.myaccount),
     path('registerUser/', views.register, name='register'),
     path('registerVendor/', views.registerVendor, name='registerVendor'),
     path('login/', views.login, name='login'),
     path('logout/', views.logout, name='logout'),
     path('myaccount/', views.myaccount, name='myaccount'),
     path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
     path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
     
     path('activate/<uidb64>/<token>/', views.activate, name='activate'),
     path('forgot_password/', views.forgot_password, name='forgot_password'),
     path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
     path('set_new_password/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),
     
     
     path('vendor/', include('vendor.urls')),
     
]
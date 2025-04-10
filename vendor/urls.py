from django.urls import path,include
from . import views
from accounts import views as AccountViews

urlpatterns = [
     path('',AccountViews.vendorDashboard, name='vendor'),
     path('profile/', views.vprofile, name='vprofile'),
     path('menu-builder/', views.menu_builder, name='menu_builder'),
     path('menu-builder/category/<int:pk>', views.fooditem_by_category, name='fooditem_by_category'),
     
     # category crud
     path('menu-builder/category/add/', views.add_category, name='add_category'),
     path('menu-builder/category/update/<int:pk>/', views.update_category, name='update_category'),
     path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
     
     # fooditem crud
     path('menu-builder/food/add/', views.add_fooditem, name='add_fooditem'),
     path('menu-builder/food/update/<int:pk>/', views.update_fooditem, name='update_fooditem'),
     path('menu-builder/food/delete/<int:pk>/', views.delete_fooditem, name='delete_fooditem'),
]
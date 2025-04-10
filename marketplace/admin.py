from django.contrib import admin
from .models import Cart
class CartAdmin(admin.ModelAdmin):
     list_display = ('user', 'fooditem', 'quantity', 'created_at', 'modified_at')    

# Register your models here.
admin.site.register(Cart,CartAdmin)
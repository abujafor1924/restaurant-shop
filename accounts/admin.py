from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class MyUserAdmin(UserAdmin):
     filter_horizontal = ('groups', 'user_permissions',)
     ordering = ('-date_joined',)
     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
     list_display = ('username', 'email', 'first_name', 'last_name','role', 'is_active')
     search_fields = ('username', 'email', 'first_name', 'last_name')
     fieldsets = (
         
     )

admin.site.register(User, MyUserAdmin)
admin.site.register(UserProfile)

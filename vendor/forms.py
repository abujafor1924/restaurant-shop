from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator


class VendorForm(forms.ModelForm):
   vendor_license =  forms.FileField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput, validators=[allow_only_images_validator])

   class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
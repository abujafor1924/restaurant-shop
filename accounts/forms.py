from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'id_address', 'placeholder': 'Start typing...', 'required': 'required'})
    )
    profile_picture = forms.FileField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
        validators=[allow_only_images_validator]
    )
    cover_picture = forms.FileField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
        validators=[allow_only_images_validator]
    )

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_picture', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Latitude & Longitude ফিল্ডকে readonly করা হয়েছে
        for field in ['latitude', 'longitude']:
            self.fields[field].widget.attrs['readonly'] = True

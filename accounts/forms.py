# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomSignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'user_type', 'profile_picture',
            'username', 'email', 'password1', 'password2',
            'address_line1', 'city', 'state', 'pincode'
        ]

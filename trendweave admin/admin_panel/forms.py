from django import forms # type: ignore
from .models import AdminRegister

class AdminRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Password input widget for security

    class Meta:
        model = AdminRegister
        fields = ['first_name', 'last_name', 'company_name', 'company_abn', 'address', 'email', 'phone_number', 'password']

from django import forms
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

#we implement our custum authentication fields for users using specific details
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'username', 'password']




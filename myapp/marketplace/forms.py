from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    username=forms.CharField(label='Name',max_length=20,required=True)
    email=forms.EmailField(label='Email',required=True)
    contact_number=forms.CharField(label='Contact Number',max_length=10,required=True)

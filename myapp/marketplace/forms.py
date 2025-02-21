from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username=forms.CharField(label='Username',max_length=20,required=True)
    email=forms.EmailField(label='Email',required=True)
    contact_number=forms.CharField(label='Contact Number',max_length=10,required=True)
    

class LoginForm(forms.Form):
    username=forms.CharField(label='Username',max_length=20,required=True)
    password=forms.CharField(label='Password',min_length=8,max_length=20,required=True)

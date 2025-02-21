from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username=forms.CharField(label='Username',max_length=20,required=True)
    email=forms.EmailField(label='Email',required=True)
    name = forms.CharField(label="Name",max_length=20,required=True)
    # contact_number=forms.CharField(label='Contact Number',max_length=10,required=True)

    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            
            raise forms.ValidationError("Username already exist")
    

class LoginForm(forms.Form):
    username=forms.CharField(label='Username',max_length=20,required=True)
    password=forms.CharField(label='Password',min_length=8,max_length=20,required=True)


class SetPasswordForm(forms.Form):
    password = forms.CharField(min_length=8,max_length=20,required=True)
    cnfrm_password = forms.CharField(min_length=8,max_length=20,required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password does not match")

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . models import Order

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

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username,password=password)

            if user is None:
                raise forms.ValidationError("Invalid Username and Password")

class SetPasswordForm(forms.Form):
    password = forms.CharField(min_length=8,max_length=20,required=True)
    cnfrm_password = forms.CharField(min_length=8,max_length=20,required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password does not match")
        

class OrderForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)
    

    class Meta:
        model = Order
        fields = ["quantity"]

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop("product", None)  # Get product instance
        super().__init__(*args, **kwargs)

        if self.product:
            self.fields["quantity"].validators.append(lambda q: self.validate_quantity(q))

    def validate_quantity(self, quantity):
        if self.product and quantity > self.product.quantity:
            raise forms.ValidationError(f"Only {self.product.quantity} kg available!")
        

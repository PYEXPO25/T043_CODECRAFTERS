from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . models import District, Order,Product, Shop,Vegetable,Rating

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
    quantity = forms.IntegerField(min_value=1,required=True)
    

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
        

class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(required=True,queryset=Vegetable.objects.all()) 
    quantity = forms.IntegerField(required=True)
    price_per_kg = forms.IntegerField(required=True)
    shop_description = forms.CharField(required=False,max_length=500)
    image = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['category', 'quantity', 'price_per_kg', 'shop_description','image']
    
    def clean(self):
        cleaned_data = super().clean()
        
        quantity = cleaned_data.get("quantity")
        price_per_kg = cleaned_data.get("price_per_kg")

        if quantity is not None and quantity <= 0:
            self.add_error("quantity", "Quantity must be greater than 0.")

        if price_per_kg is not None and price_per_kg <= 0:
            self.add_error("price_per_kg", "Price per kg must be greater than 0.")

        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=False)
        cleaned_data = self.cleaned_data
        
        if cleaned_data.get("image"):
            product.image = cleaned_data["image"]
        elif cleaned_data.get("category"):  # Ensure category exists before accessing default_image
            product.image = cleaned_data["category"].default_image

        if commit:
            product.save()

        return product
    

class AddReviewForm(forms.ModelForm):
    review = forms.CharField(required=True)
    rating = forms.IntegerField(min_value=0,max_value=5,required=True)

    class Meta:
        model = Rating
        fields = ['review','rating']

    def save(self, commit = ...):
        review = super().save(commit)

        return review
    
    def clean(self):
        cleaned_data =  super().clean()
        

class EditProductForm(forms.ModelForm):
    price_per_kg = forms.IntegerField(required=True)
    quantity = forms.IntegerField(required=True)
    description = forms.CharField(required=True)
    class Meta:
        model = Product
        fields = ['price_per_kg', 'quantity', 'description']

class NewShopForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=50)
    district = forms.ModelChoiceField(required=True,queryset=District.objects.all())
    image = forms.ImageField(required=False)
    shop_description = forms.CharField(max_length=1500,required=False)

    class Meta:
        model = Shop
        fields = ['image','shop_description','district','name']

    def save(self, commit = ...):
        shop = super().save(commit)
        
        if commit:
            shop.save()
        return shop
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email",required=True)

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")

        if not User.objects.filter(email = email).exists:

            raise forms.ValidationError("Invalid email")
        
class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=20,label="New password",required=True)
    confirm_password = forms.CharField(max_length=20,label="Confirm password",required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        cnfrm_password = cleaned_data.get('confirm_password')

        if password and cnfrm_password and password != cnfrm_password:
            raise forms.ValidationError("Password Doesn't match")
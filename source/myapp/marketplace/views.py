from django.shortcuts import render,redirect, get_object_or_404
from django.http.response import HttpResponse
from . forms import RegisterForm,SetPasswordForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Product, Shop, temp_user,Vegetables
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
from django.db.models import Q
# Create your views here.

def index(request):
    
    search = request.GET.get('query', '').strip()
    search_terms = search.split()
    
    shop_query = Q()   # For searching shops
    product_query = Q() # For searching products

    if search:
        # 🔹 Step 1: Find matching vegetable IDs
        vegetable_matches = Vegetables.objects.filter(vegetable__icontains=search).values_list('id', flat=True)

        for term in search_terms:
            shop_query |= Q(shop_name__icontains=term)  # Search in Shop
            product_query |= Q(category_id__in=vegetable_matches) | Q(shop_name__shop_name__icontains=term)  

        # 🔹 Step 2: Search for products and shops separately
        products = Product.objects.filter(product_query)
        shops = Shop.objects.filter(is_available=True).filter(shop_query)

        if not products and not shops:
            messages.warning(request, "No results found")
    else:
        shops = Shop.objects.filter(is_available=True)
        products = Product.objects.all()

    paginator = Paginator(shops, 3)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)

    return render(request, 'marketplace/index.html', {
        'style': 'index',
        'title': 'Home Page',
        'page_obj': page_obj,
        'products': products
    })




def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                
                email = form.cleaned_data['email']
                
                name = form.cleaned_data['name']
                username = form.cleaned_data['username']
                
                token = str(uuid.uuid4())  # Generate a unique token
                user = temp_user.objects.create(email=email, name=name, token=token,username = username)
                
                
                subject = "Password Change Request"
                current_site = get_current_site(request)
                domain = current_site.domain
                
                message = render_to_string("marketplace/verifyemail.html", {
                    "domain": domain,
                    "token": user.token,
                    "name": name
                })
                
                print(message)
                send_mail(subject, message, "noreply@zoro.com", [email], fail_silently=False)
                messages.success(request, "Verification Email has been sent to your mail")
                
                return redirect('marketplace:register')  # Redirect to avoid resubmission
            except Exception as e:
                print(e)
                messages.warning(request, "Something went wrong. Try again.")
    
    return render(request, 'marketplace/register.html', {'form': form,'title':'Register','style':'forms'})


def set_password(request, token):
    Temp_user = get_object_or_404(temp_user, token=token)
    form = SetPasswordForm()
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        
        if form.is_valid():
            print("Here")
            password = form.cleaned_data['password']
            print(password)
            user = User.objects.create(
                username=Temp_user.username,
                email=Temp_user.email,
                first_name=Temp_user.name,
                password=make_password(password)
            )
            
            Temp_user.delete()  
            
            return redirect(reverse('marketplace:login')) 

    return render(request, 'marketplace/set_password.html', {'email': temp_user.email,'title':'Set Password','style':'forms'})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect(reverse("marketplace:index"))

    return render(request,"marketplace/login.html",{'title':'Login','form':form,'style':'forms'})

def view_shop(request,slug):
    shop = Shop.objects.get(slug=slug)
    products = Product.objects.filter(shop_name=shop)
    paginator = Paginator(products,3)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    return render(request,"marketplace/viewshop.html",{'style':'viewshop','shop':shop,"page_obj":page_obj})


def logout_view(request):
    logout(request)
    return redirect("blog:index")

def showproduct(request,shopname,product):
    
    return render(request,'marketplace/productdetail.html',{'shop':shopname,'product':product})
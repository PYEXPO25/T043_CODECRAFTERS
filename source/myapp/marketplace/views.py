from django.shortcuts import render,redirect, get_object_or_404
from django.http.response import HttpResponse,HttpResponseRedirect
from . forms import RegisterForm,SetPasswordForm,LoginForm,OrderForm
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Product, Shop, TempUser,Vegetable
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
from django.db.models import Q
# Create your views here.

def index(request):
    
    search = request.GET.get('query', '')
    
    if search:
        return redirect(reverse("marketplace:search"))
    
    shops = Shop.objects.filter()
    products = Product.objects.all()

    paginator = Paginator(shops, 9)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)

    return render(request, 'marketplace/index.html', {
        'style': 'index',
        'title': 'Home Page',
        'page_obj': page_obj,
        'products': products
    })




def search_results(request):
    query = request.GET.get('q', '')
    selected_categories = request.GET.getlist('category')
    selected_districts = request.GET.getlist('district')
    sort_option = request.GET.get('sort', 'price_low')
    
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(shop__name__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)
    
    if selected_districts:
        products = products.filter(shop__district__in=selected_districts)
    
    if sort_option == 'price_low':
        products = products.order_by('price_per_kg')
    elif sort_option == 'price_high':
        products = products.order_by('-price_per_kg')
    elif sort_option == 'name_az':
        products = products.order_by('name')
    elif sort_option == 'name_za':
        products = products.order_by('-name')
    
    categories = Vegetable.objects.all()
    districts = Shop.objects.values_list('district', flat=True).distinct()
    
    return render(request, 'marketplace/search_results.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'districts': districts,
        'selected_categories': selected_categories,
        'selected_districts': selected_districts,
        'sort_option': sort_option
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
                user = TempUser.objects.create(email=email, name=name, token=token,username = username)
                
                
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
    Temp_user = get_object_or_404(TempUser, token=token)
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

    return render(request, 'marketplace/set_password.html', {'email': TempUser.email,'title':'Set Password','style':'forms'})


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
    products = Product.objects.filter(shop=shop)
    paginator = Paginator(products,3)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    return render(request,"marketplace/viewshop.html",{'style':'viewshop','shop':shop,"page_obj":page_obj})


def logout_view(request):
    logout(request)
   
    return redirect(reverse("marketplace:index"))



def showproduct(request, shopslug, product):
    product = get_object_or_404(Product, slug=product)
    shop = get_object_or_404(Shop, slug=shopslug)
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.total_price = order.quantity * product.price_per_kg

            
            if product.quantity >= order.quantity:
                product.quantity -= order.quantity
                product.save()

                order.save()
                messages.success(request, "Your order has been successfully placed!")
                return redirect(reverse("marketplace:showproduct", kwargs={"shopslug": shopslug, "product": product.slug}))

            else:
                messages.error(request, "Insufficient stock available!")

    return render(request, 'marketplace/productdetail.html', {'shop': shop, 'product': product, 'form': form})



def myshops(request):

    myshops = Shop.objects.filter(shop_owner = request.user)
    return render(request,"marketplace/myshops.html",{})
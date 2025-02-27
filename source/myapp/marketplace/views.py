from django.shortcuts import render,redirect, get_object_or_404
from django.http.response import HttpResponse,HttpResponseRedirect
from . forms import RegisterForm,SetPasswordForm,LoginForm,OrderForm,AddProductForm,AddReviewForm,EditProductForm,NewShopForm,ForgotPasswordForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Product, Rating, Shop, TempUser,Vegetable,District,Order
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
from django.db.models import Q
from django.utils.translation import gettext as _
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    
    query = request.GET.get('q', '')  # Get search query from request
    if query:
        return redirect(f"{reverse('search_results')}?q={query}")
    
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
    
    products = Product.objects.filter(is_available = True)
    
    if query:
        
        products = products.filter(
            
            Q(shop__name__icontains=query) |
            Q(category__name__icontains=query)|
            Q(shop__district__name__icontains=query)
        )
    
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)
    
    if selected_districts:
        products = products.filter(shop__district__in=selected_districts)
    
    if sort_option == 'price_asc':
        products = products.order_by('price_per_kg')
    elif sort_option == 'price_desc':
        products = products.order_by('-price_per_kg')
    
    
    categories = Vegetable.objects.all()
    districts = District.objects.all()
    
    return render(request, 'marketplace/search.html', {
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
    products = Product.objects.filter(shop=shop,is_available = True)
    
    paginator = Paginator(products,3)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    form = AddReviewForm()
    if request.method == "POST":
        rating_value = int(request.POST.get("rating"))
        review_text = request.POST.get("review")

        if request.user.is_authenticated:
            if Rating.objects.filter(shop=shop, user=request.user).exists():
                messages.error(request, "You have already submitted a review for this shop.")
                return redirect(reverse('marketplace:shop',kwargs={'slug':slug}))

            # Create a new rating
            Rating.objects.create(shop=shop, user=request.user, rating=rating_value, review=review_text)
            messages.success(request, "Your review has been submitted.")

        else:
            messages.error(request, "You need to be logged in to submit a review.")
            return redirect(reverse('marketplace:login'))
        return redirect(reverse('marketplace:shop',kwargs={'slug':slug}))
    return render(request,"marketplace/viewshop.html",{'style':'viewshop','shop':shop,"page_obj":page_obj,'form':form})

@login_required
def logout_view(request):
    logout(request)
   
    return redirect(reverse("marketplace:index"))






@login_required
def myshops(request):
    myshops = Shop.objects.filter(shop_owner = request.user)
    return render(request,"marketplace/myshops.html",{"myshops":myshops})

@login_required
def addproduct(request,shopname):
    shop = Shop.objects.get(name=shopname)
    form = AddProductForm()
    if request.method == "POST":
        print("POST DATA:", request.POST)

        form = AddProductForm(request.POST,request.FILES)
        print(form.errors)

        if form.is_valid():
            print("Valid")
            product = form.save(commit=False)
            product.shop = shop
            product.shop_description = f"Buy this Fresh and high-quality {form.cleaned_data['category']} at {shop.name}."
            product.save()
            messages.success(request,"Shop has been Created!")
            return redirect(reverse('marketplace:shop', kwargs={'slug': shop.slug}))  # Change to your success URL
    vegetables = Vegetable.objects.all()

    return render(request,"marketplace/addproduct.html",{'vegetables':vegetables,'form':form})

@login_required
def myorders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,"marketplace/myorders.html",{'orders':orders})

def deleteproduct(request,productslug):
    product = Product.objects.get(slug=productslug)
    product.delete()
    return redirect(reverse("marketplace:myorders")) 

@login_required
def edit_product(request, shopslug, product):
    product = get_object_or_404(Product, slug=product)
    shop = get_object_or_404(Shop,slug=shopslug)
    if request.method == "POST":
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product detail updated successfully.")
            return redirect('marketplace:showproduct', shop.slug, product.slug)  # Redirect after successful edit
    else:
        form = EditProductForm(instance=product)

    return render(request, 'marketplace/editproduct.html', {'form': form, 'product': product})

@login_required
def remove_product(request, shopslug, product):
    product_instance = get_object_or_404(Product, shop__slug=shopslug, slug=product)
    product_instance.is_available =False
    product_instance.save()
    messages.success(request, "Product removed successfully.")
    return redirect("marketplace:shop", slug=shopslug)

@login_required
def add_shop(request):
    form = NewShopForm()
    districts = District.objects.all()
    if request.method == 'POST':
        form = NewShopForm(request.POST,request.FILES)
        print('Here')
        if form.is_valid():
            print('Valid')
            shop = form.save(commit=False)
            shop.shop_owner = request.user
            shop.save()
            return redirect(reverse('marketplace:shop',kwargs={'slug':shop.slug}))
    return render(request,"marketplace/addshop.html",{'districts':districts,"form":form})

def forgotpassword(request):

    form = ForgotPasswordForm()

    if request.method == 'POST':

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                user = User.objects.get(email=email)
                subject = "Password Change request"
                current_site = get_current_site(request)
                
                domain = current_site.domain
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                message = render_to_string("marketplace/forgetpasswordemail.html",{"domain":domain,"uid":uid,"token":token})
                
                send_mail(subject,message,"noreply@zoro.com",[email])
                messages.success(request,"Verification Email has been sent your mail")
            except Exception as e:
                
                messages.warning(request,e)
                
    return render(request,"marketplace/forgetpassword.html",{'title':"Forgot Password","form":form})



def resetpassword(request,uidb64,token):
    form = SetPasswordForm()
    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        
        if form.is_valid():
            new_pass = form.cleaned_data['password']
            try:
                pk = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=pk)
            except:
                user = None

            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_pass)
                user.save()
                messages.success(request,"Your password has been successfully updated.")
                return redirect(reverse('marketplace:index'))
            else:
                messages.error(request,"Your redirect link has been expired")

    return render(request,"marketplace/set_password.html",{"title":"Reset password",'form':form})




def showproduct(request, shopslug, product):
    product = get_object_or_404(Product, slug=product)
    shop = get_object_or_404(Shop, slug=shopslug)
    form = OrderForm()
    
    if product.is_available:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                if not request.user.is_authenticated:
                    messages.error(request, "You need to be logged in to purchase a product.")
                    return redirect(reverse('marketplace:login'))

                quantity = form.cleaned_data['quantity']
                amount = quantity * product.price_per_kg * 100  # Razorpay requires amount in paise
                
                # Save order without updating product quantity
                order = form.save(commit=False)
                order.user = request.user
                order.product = product
                order.total_price = amount//100
                order.shop = shop
                order.is_paid = False  # New field to track payment status
                order.save()

                # Redirect to payment
                return redirect(reverse("marketplace:payment", kwargs={'shopslug': shop.slug, 'product': product.slug, "amount": int(amount), 'order_id': order.id}))


        return render(request, 'marketplace/productdetail.html', {'shop': shop, 'product': product, 'form': form})
    
    return redirect(reverse('marketplace:shop', kwargs={'slug': shop.slug}))

def payment(request,shopslug,product,amount,order_id):
    if request.method == 'POST':
        client = razorpay.Client(auth=('rzp_test_ZaxbrIIi7xfJQ5','TzfugBDqIED2MC0Wk9oXsWsA'))
        payment = client.order.create({"amount":amount,'currency':'INR','payment_capture':'1'})
    return render(request,'marketplace/payment.html',{"amount":amount,'shopslug':shopslug,"product":product})


@csrf_exempt
def sucess(request, shopslug, product, order_id,amount):
    order = get_object_or_404(Order, id=order_id, product__slug=product, shop__slug=shopslug)

    if not order.is_paid:  # Check if order was already processed
        order.is_paid = True
        order.save()
        
        product = order.product
        if product.quantity >= order.quantity:
            product.quantity -= order.quantity
            if product.quantity == 0:
                product.is_available = False
            product.save()

        messages.success(request, "Payment successful! Your order has been confirmed.")

    return redirect(reverse('marketplace:myorders'))


def cancel(request,shopslug,product):
    
    messages.warning(request,'Your payment has been canceled')
    return redirect(reverse('marketplace:showproduct',kwargs={"shopslug":shopslug,'product':product}))
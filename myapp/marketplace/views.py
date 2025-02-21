from django.shortcuts import render,redirect, get_object_or_404
from django.http.response import HttpResponse
from . forms import RegisterForm,SetPasswordForm,LoginForm
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.contrib import messages
from .models import temp_user
from django.contrib.auth.models import User
import uuid
from django.urls import reverse

# Create your views here.

def index(request):
    return HttpResponse("Index")




def log_out(request):
    pass



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
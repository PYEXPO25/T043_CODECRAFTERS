from django.shortcuts import render,redirect, get_object_or_404
from django.http.response import HttpResponse
from . forms import RegisterForm
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib import messages
from .models import temp_user
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return HttpResponse("Hello world")


def login(request):
    return HttpResponse('Log in')

def log_out(request):
    pass

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            try:
                email = request.POST['email']
                name = request.POST['name']
                
                subject = "Password Change request"
                current_site = get_current_site(request)
                token = request.POST['token']
                domain = current_site.domain
                
                message = render_to_string("blog/email.html",{"domain":domain,'token':token,"name":name})
                
                send_mail(subject,message,"noreply@zoro.com",[email])
                messages.success(request,"Verification Email has been sent your mail")
            except Exception as e:
                messages.warning(request,"No email exist")

    return render(request,'marketplace/register.html')

def set_password(request, token):
    temp_user = get_object_or_404(temp_user, token=token)

    if request.method == 'POST':
        password = request.POST['password']
        
        user = User.objects.create(
            username=temp_user.username,
            email=temp_user.email,
            first_name=temp_user.full_name,
            password=set_password(password)
        )
        
        temp_user.delete()  
        
        return redirect(reverse('blog:login')) 

    return render(request, 'set_password.html', {'email': temp_user.email})
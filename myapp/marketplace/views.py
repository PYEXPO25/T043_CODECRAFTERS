from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello world")
def log_out(request):
    pass
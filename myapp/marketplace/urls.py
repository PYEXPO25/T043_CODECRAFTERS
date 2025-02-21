from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name='register'),
    path('setpassword/<str:token>',views.set_password,name='setpassword')
]

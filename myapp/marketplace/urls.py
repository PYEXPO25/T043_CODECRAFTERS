from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name='register'),
    path('setpassword/<token>',views.set_password,name='setpassword')
]

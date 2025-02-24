from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name='register'),
    path('setpassword/<str:token>',views.set_password,name='setpassword'),
    path('login/',views.login_view,name="login"),
    path('shop/<str:slug>',views.view_shop,name="shop"),
    path('logout/',views.logout_view,name="log_out"),
    path('<shopslug>/<product>/',views.showproduct,name="showproduct"),
    path('myshops/',views.myshops,name="myshops"),
    path('search/',views.search_results,name="search"),
]

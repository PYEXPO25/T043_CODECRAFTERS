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
    path('my_shops/',views.myshops,name="myshops"),
    path('search/',views.search_results,name="search"),
    path('<shopname>/addproduct',views.addproduct,name="addproduct"),
    path('myorders/',views.myorders,name="myorders"),
    path('delete_product/<productslug>/',views.deleteproduct,name="deleteproduct"),
    path('<shopslug>/edit/<product>/',views.edit_product,name="editproduct"),
    path("shop/<slug:shopslug>/product/<slug:product>/remove/", views.remove_product, name="removeproduct"),
    path('my_shops/new_shop',views.add_shop,name="addshop"),
    path("forgotpassword/",views.forgotpassword,name="forgotpassword"),
    path("resetpassword/<uidb64>/<token>",views.resetpassword,name="resetpassword"),
    path('<slug:shopslug>/<slug:product>/payment/<int:amount>/<int:order_id>/', views.payment, name='payment'),
    path('<slug:shopslug>/<slug:product>/payment/<int:amount>/<int:order_id>/sucess', views.sucess, name='success'),
    path('cancel/<shopslug>/<product>/',views.cancel,name="cancel"),
]

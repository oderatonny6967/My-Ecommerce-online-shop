from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
     path('index2/', views.index2, name='index2'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_history/', views.order_history, name='order_history'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
      path('search/', views.product_search, name='product_search'),
    path('register/', views.register, name='register'),
     path('checkout2/', views.checkout, name='checkout'),
    path('payment/mpesa/', views.mpesa_payment, name='mpesa_payment'),
    path('payment/visa/', views.visa_payment, name='visa_payment'),
    path('payment/paypal/', views.paypal_payment, name='paypal_payment'),
]

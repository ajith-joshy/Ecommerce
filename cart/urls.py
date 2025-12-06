"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
app_name="cart"
from cart import views

urlpatterns = [
    path('addtocart/<int:i>',views.Addtocart.as_view(),name="addtocart"),
    path('cartview',views.Cart_view.as_view(),name="cartview"),
    path('remove/<int:i>',views.Removefromcart.as_view(),name="remove"),
    path('delete/<int:i>',views.Deletefromcart.as_view(),name="delete"),
    path('checkout',views.Checkout.as_view(),name="checkout"),
    path('payment_success',views.Payment_success.as_view(),name="payment_success"),
    path('your_orders',views.Your_orders.as_view(),name="your_orders"),
]

from django.conf.urls.static import static
from django.conf import settings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
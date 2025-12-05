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
app_name="shop"
from shop import views

urlpatterns = [
    path('',views.Category_view.as_view(),name="categories"),
    path('products/<int:i>',views.Product_view.as_view(),name="products"),
    path('detail/<int:i>',views.Detail_view.as_view(),name="detail"),
    path('register',views.Register.as_view(),name="register"),
    path('login',views.Userlogin.as_view(),name="login"),
    path('logout',views.Userlogout.as_view(),name="logout"),
    path('category',views.Add_category.as_view(),name="category"),
    path('product',views.Add_product.as_view(),name="product"),
    path('add/<int:i>',views.Add_stock.as_view(),name="add")
]


from django.conf.urls.static import static
from django.conf import settings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
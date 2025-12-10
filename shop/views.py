from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Category
from django.contrib.auth import authenticate,login,logout


# Create your views here.
class Category_view(View):
    def get(self,request):
        c=Category.objects.all()
        context={'cat':c}
        return render(request,'categories.html',context)

class Product_view(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'cat':c}
        return render(request,'products.html',context)

from .models import Product
class Detail_view(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'detail.html',context)

class Register(View):
    def get(self,request):
        f=Registerform()
        context={'form':f}
        return render(request,'register.html',context)
    def post(self,request):
        f=Registerform(request.POST)
        if f.is_valid():
            f.save()
        print(request.POST)
        return redirect('shop:login')

from django.contrib import messages
from .forms import Loginform, Registerform
class Userlogin(View):
    def get(self,request):
        f=Loginform()
        context={'form':f}
        return render(request,'login.html',context)
    def post(self,request):
        f=Loginform(request.POST)
        if f.is_valid():
            data=f.cleaned_data #Fetch the data after validation
            u=data['username']  #retrieve username from cleaned_data
            p=data['password']  #retrieve password from cleaned_data
            user=authenticate(username=u,password=p)    #Calls authenticate() to verify if user exists
                                                        #if record exists then it returns user object
                                                        #else none
            if user:    #if user exists
                login(request,user)     #adds the user into current session
                return redirect('shop:categories')
            else:   #if user does not exist
                messages.error(request, "Invalid credentials")
                return redirect('shop:login')

from django.contrib.auth.decorators import login_required
from .forms import Categoryform,Productform

from django.http import HttpResponse
def admin_required(fun):
    def wrapper(request):
        if not request.user.is_superuser:
            return HttpResponse("not allowed")
        else:
            return fun(request)
    return wrapper

@method_decorator(admin_required,name="dispatch")
@method_decorator(login_required,name="dispatch")
class Add_category(View):
    def get(self, request):
        cf = Categoryform()
        context = {'cform': cf }
        return render(request, 'addcategory.html', context)
    def post(self, request):
        cf = Categoryform(request.POST,request.FILES)
        if cf.is_valid:
            cf.save()
        return render(request, 'addcategory.html')

@method_decorator(login_required,name="dispatch")
class Add_product(View):
    def get(self, request):
        pf = Productform()
        context = {'pform': pf}
        return render(request, 'addproduct.html', context)
    def post(self, request):
        pf = Productform(request.POST,request.FILES)
        if pf.is_valid():
            pf.save()
        return render(request, 'addproduct.html')

from .forms import Stockform
class Add_stock(View):
    def get(self,request,i):
        b=Product.objects.get(id=i)
        f=Stockform(instance=b)
        context={'form':f}
        return render(request,'edit.html',context)
    def post(self,request,i):
        b=Product.objects.get(id=i)
        f=Stockform(request.POST,instance=b)
        if f.is_valid():
            f.save()
        return redirect('shop:categories')

class User_view(View):
    def get(self,request):
        return render(request,'userhome.html')

class Userlogout(View):
    def get(self,request):
        logout(request) #removes the user from current session
        return redirect('shop:login')

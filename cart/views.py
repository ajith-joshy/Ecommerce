import razorpay
from django.shortcuts import render,redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from shop.models import Product
from cart.models import Cart
class Addtocart(View):
    def get(self,request,i):
        #product
        p=Product.objects.get(id=i)
        #user
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)    #if yes
            c.quantity+=1   #increments quantity by 1
            c.save()
        except:             #if product does not exist
            c=Cart.objects.create(user=u,product=p,quantity=1)  #creates a new record with quantity=1
            c.save()
        return redirect('cart:cartview')

class Removefromcart(View):
    def get(self,request,i):
        try:
            c=Cart.objects.get(id=i)
            if c.quantity>1:
                c.quantity-=1
                c.save()
            else:
                c.delete()
        except:
            pass
        return redirect('cart:cartview')

class Deletefromcart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        p.delete()
        return redirect('cart:cartview')
#     OR
#       try:
#             c=Cart.objects.get(id=i)

class Cart_view(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+i.sub_total()
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)

import uuid
from .forms import Orderform
class Checkout(View):
    def get(self,request):
        f=Orderform()
        context={'form':f}
        return render(request,'checkout.html',context)
    def post(self,request):
        f=Orderform(request.POST)
        if f.is_valid():
            o=f.save(commit=False)
            #adds current user
            u=request.user
            o.user=u
            #adds total amount
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.sub_total()
            print(total)
            o.amount=total
            o.save()
            # ONLINE
            if o.payment_method=="ONLINE":
                #1.Create a razorpay connection using Keys
                client=razorpay.Client(auth=('rzp_test_Rn84rIATO1bxPq','UMv2lXUOvwRtcka3W2dELzO4'))
                #2.Creates a new order in razorpay
                response_payment=client.order.create({'amount':(o.amount)*100,'currency':'INR'})
                print(response_payment)
                #retreives the order id from the response_payment
                id=response_payment['id']
                #saves it in the order table
                o.order_id=id
                o.save()
                context={'payment':response_payment}
                return render(request,'payment.html',context)
            else:   #COD
                id='ORD_COD'+uuid.uuid4().hex[:14]
                o.order_id=id
                o.is_ordered=True
                o.save()
            #add products to Order_items
            for i in c:
                item = Order_items.objects.create(order=o, product=i.product, quantity=i.quantity)
                item.save()
                item.product.stock -= i.quantity
                item.product.save()
            # Delete Cart Table
            c.delete()
            return render(request,'payment.html')

# @csrf_exempt
# def f():
#     pass

#CSRF_EXEMPT -to ignore csrf verification for this view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Order,Order_items
@method_decorator(csrf_exempt,name="dispatch")
class Payment_success(View):
    def post(self,request):
        print(request.user.username)
        response=request.POST
        # print(response)

        #Updates Order Table
        id=response['razorpay_order_id']    #reads the order id from the razorpay response
        o=Order.objects.get(order_id=id)    #retreieves the order record matching with the order id
        o.is_ordered=True   #Set is_ordered status to True
        o.save()

        #Add products into Order_items Table
        u=request.user
        c=Cart.objects.filter(user=u)
        for i in c:
            item=Order_items.objects.create(order=o,product=i.product,quantity=i.quantity)
            item.save()
            item.product.stock-=i.quantity
            item.product.save()
        #Delete Cart Table
        c.delete()
        return render(request,'payment_success.html')

class Your_orders(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'your_orders':o}
        return render(request,'your_orders.html',context)


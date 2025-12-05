from tkinter.font import names

from django.shortcuts import render
from django.views import View

# Create your views here.
from django.db.models import Q
from shop.models import Product
class Search_view(View):
    def get(self,request):
        query=request.GET['q']      #reads the keyword
        print(query)
        #ORM query to filter records from table(two or more records)
        p=Product.objects.filter(Q(name__icontains=query)|
                              Q(description__icontains=query)|
                              Q(image__icontains=query)|
                              Q(price__icontains=query)|
                              Q(stock__icontains=query)|
                              Q(available__icontains=query))
        #case insensitive
        context={'products':p,'query':query}
        return render(request,'search.html',context)

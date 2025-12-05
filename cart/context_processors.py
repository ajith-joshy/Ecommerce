from .models import Cart
def count(request):
    total=0
    if request.user.is_authenticated:
        u=request.user
        try:
            c=Cart.objects.all()
            for i in c:
                total=total+i.quantity
        except:
            pass
    return{'count':total}
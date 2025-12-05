from django import forms
from .models import Order

class Orderform(forms.ModelForm):
    payment_choices=(('COD','COD'),('ONLINE','ONLINE'))
    payment_method=forms.ChoiceField(choices=payment_choices)
    class Meta:
        model=Order
        fields=['address','phone','payment_method']

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Registerform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2','email','first_name','last_name']

class Loginform(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

from .models import Category
class Categoryform(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"

from .models import Product
class Productform(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','description','price','image','stock','category']

class Stockform(forms.ModelForm):
    class Meta:
        model=Product
        fields=['stock']
from django.shortcuts import render, redirect
from product.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import *
from . models import *


# Create your views here.

def homepage(request):
    product = Product.objects.all().order_by('-id')[:4]
# [:4] le chai 4 ota product matra dekhauxa homepage ma 
# .order_by('-id')[:4] le last bata 4 ota product dekhauxa
    context = {
        'product': product
    }
    return render(request, 'users/index.html', context)
# Product vanne model bata sabai data lai product vanne ma access garyo ani context ma rakhera html ma render garera pathayo
def productpage(request):
    product = Product.objects.all().order_by('-id')[:8]

    context = {
        'product': product
    }
    return render(request, 'users/products.html', context)

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'users/productdetail.html', context)

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Account created successfully')
            return redirect('/register')
        else:
            messages.add_message(request, messages.ERROR, 'Kindly verify all the fields')
            return render(request, 'users/register.html', {'form': form} )
    context = {
        'form':UserCreationForm
    }
    return render(request, 'users/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # form.cleaned_data LE FORM BATA AKO DATA LAI READ GARXA
            user = authenticate(username =data['username'], password= data['password'])
            # user = authenticate vanne line le chai form bata ako username ra password lai database ma vako username pswrod sng check garxa
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('/admins')
                else:
                    return redirect('/') 
            else:
                messages.add_message(request, messages.ERROR, 'kindly check all the fields')
                return render(request, 'users/login.html', {'form':form})

    context = {
        'form': LoginForm
    }
    return render(request, 'users/login.html', context)

# context le chai views bata form lai template ma pathauxa users/login.html ma

def logout_user(request):
    logout(request)
    return redirect('/login')

def add_to_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    user = request.user

    check_item_presence = Cart.objects.filter(user= user, product= product)
    if check_item_presence:
        messages.add_message(request, messages.ERROR, 'Product is already presented in the cart')
    else:
        Cart.objects.create(user=user, product =product)
        messages.add_message(request, messages.SUCCESS, 'product is added successfully in cart')
        return redirect('/cart')
    
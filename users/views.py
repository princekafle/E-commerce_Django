from django.shortcuts import render, redirect
from product.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import *
from . models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from . filters import *


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
    user = request.user.id
    items = Cart.objects.filter(user= user)
    # mathy ko duita line chai cart iems ko nbr display garauna lai rakheko 

    product = Product.objects.all().order_by('-id')
    product_filter = ProductFilter(request.GET, queryset = product)
    product_new = product_filter.qs

    pages = Paginator(product_new,2)
    pagenumber = request.GET.get('page')
    # pagenumber = request.GET.get('page') le url bata page number linxa 
    productfinal = pages.get_page(pagenumber)

    # productfinal = paginator.get_page(pagenumber) le pagenumber ma vayeko product dekhauxa productfinal ko through bata
    

    context = {
        'product':productfinal,
        'product_filter': product_filter,
        'items': items
        
    }
    return render(request, 'users/products.html', context)

def product_detail(request, product_id):
    user = request.user.id
    items = Cart.objects.filter(user= user)
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
        'items': items
               }
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

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    user = request.user
    # This retrieves the current logged-in user from the request

    check_item_presence = Cart.objects.filter(user=user, product=product)
    # yesle cart ma vayeko product ra user ani add to cart request garne user ra product lai check garxa

    if check_item_presence:
        messages.add_message(request, messages.ERROR, f'{product.product_name} is already presented in the cart')
        return redirect(f'/productdetail/{product_id}')
    else:
       cart=  Cart.objects.create(user= user, product = product)
       if cart:
            messages.add_message(request, messages.SUCCESS, 'product added successfully in cart')
            return redirect('/cart')
       else:
            messages.add_message(request, messages.ERROR,'Error while adding in cart')
@login_required
def viewcart(request):
    user = request.user.id
    items = Cart.objects.filter(user= user)
    # mathy ko line le chai jun user le cart create gareko xa tesle maatra cart herna pauxa
    context = {
        'items': items
    }
    return render(request, 'users/cart.html', context)

@login_required
def deletecart(request, cart_id):
    item= Cart.objects.get(id = cart_id)
    item.delete()
    messages.add_message(request, messages.ERROR, 'Product deleted form the cart ')
    return redirect('/cart')

@login_required
def order(request, product_id, cart_id):
    user = request.user
    product = Product.objects.get(id = product_id)
    cart = Cart.objects.get(id = cart_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        quantity = request.POST.get('quantity')
        price = product.product_price
        total_price = int(quantity)*int(price)
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user = user,
            product = product,
            quantity = quantity,
            total_price = total_price,
            contact_no = contact_no,
            address = address,
            payment_method = payment_method

        )
        # //mathy request.method == 'POST': bata aako user le haleko data chai model ma haleko ho
        # quantity = quantity vaneko quantity vaneko form bata ako data ra arko quantity vaneko model ma banako quantity
        if order.payment_method == 'Cash on Delivery':
            cart.delete()
            messages.add_message(request, messages.SUCCESS, 'your order has been successfully ordered')
            return redirect('/myorder')
    context = {
        'form': OrderForm
    }
    return render(request, 'users/order.html', context)
@login_required
def myorder(request):
    user = request.user
    order= Order.objects.filter(user=user)
    context = {
        'order': order
    }
    return render(request, 'users/myorder.html', context)
    
    

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.auth import admin_only


def index(request):
    return HttpResponse("Welcome to product page")

def home(request):
    product = Product.objects.all()
    context = {
        "product": product
    }
    return render(request, 'products/index.html', context)

@login_required
@admin_only
def productlist(request):
    product = Product.objects.all()
    context = {
        "product": product
    }

    return render(request, 'products/allproducts.html', context)

@login_required
@admin_only
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Added Product successfully')
            return redirect('/product/addproduct')  # Ensure the correct path for redirection
        else:
            messages.add_message(request, messages.ERROR, 'Kindly verify all the fields')
            return render(request, 'products/addproduct.html', {"form": form})
    context = {
        'form': ProductForm
    }
    return render(request, 'products/addproduct.html', context)

@login_required
@admin_only
def add_category(request):
    if request.method == "POST":
        form =CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Added Category successfully')
            return redirect('/product/addcategory')  
        else:
            messages.add_message(request, messages.ERROR, 'Kindly verify all the fields')
            return render(request, 'products/addcategory.html', {"form": form})
    
    context = {
        'form':CategoryForm
    }
    return render(request, 'products/addcategory.html', context)

@login_required
@admin_only
def update_product(request, product_id):
    instance = Product.objects.get(id= product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance= instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product updated successfully')
            return redirect('/product/productlist')
        else:
            messages.add_message(request, messages.ERROR, 'Kindly verify all the fields ')
            return render(request, 'products/updateproduct.html', {'form': form})
    context = {
        'form': ProductForm(instance=instance)
    }
    return render(request, 'products/updateproduct.html', context)

@login_required
@admin_only
def delete_product(request, product_id):
    instance = Product.objects.get(id= product_id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS, 'Product deleted successfully')
    return redirect('/product/productlist')

@login_required
@admin_only
def category_list(request):
    category = Category.objects.all()
    context  = {
        'category':category
    }
    return render(request, 'products/allcategory.html', context)

@login_required
@admin_only
def update_category(request, category_id):
    instance = Category.objects.get(id= category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance= instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category updated successfully')
            return redirect('/product/categorylist')
        else:
            messages.add_message(request, messages.ERROR, 'Kindly verify all the fields ')
            return render(request, 'products/updatecategory.html', {'form': form})
    context = {
        'form': CategoryForm(instance=instance)
    }
    return render(request, 'products/updatecategory.html', context)

@login_required
@admin_only
def delete_category(request, category_id):
    instance = Category.objects.get(id= category_id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS, 'Category deleted successfully')
    return redirect('/product/categorylist')


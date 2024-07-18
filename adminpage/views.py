from django.shortcuts import render
from django.http import HttpResponse

def admin_page(request):
    return render(request,'admins/admin.html')

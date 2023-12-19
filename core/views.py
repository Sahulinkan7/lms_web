from django.shortcuts import render
from storeapp.models import Categories
from storeapp.models import Course
import socket
def home_view(request):
    domain=request.get_host()
    print(domain)
    categories=Categories.objects.all()
    courses=Course.objects.filter(status='PUBLISH')
    context={'categories':categories,'courses':courses}
    return render(request,"core/home.html",context)

def error_view(request):
    return render(request,"core/error_404.html")

def about_us(request):
    return render(request,"core/about_us.html")

def contact_us(request):
    return render(request,"core/contact_us.html")
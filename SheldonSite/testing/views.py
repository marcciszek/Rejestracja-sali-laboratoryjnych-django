from django.shortcuts import render

# Create your views here.

def index(req):
    return render(req,'index.html')

def login(req):
    return render(req,'login.html')

def login2(req):
    return render(req,'login2.html')

def register(req):
    return render(req,'register.html')

def lista(req):
    return render(req,'listing.html')

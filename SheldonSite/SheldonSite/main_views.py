from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
    return render(request, 'mainpage/mainpage.html')

def infopage(request):
    return render(request,'infopage.html')

def contact(request):
    return render(request,'contact.html')
from django.contrib.auth import logout
from django.shortcuts import render

def logout(request):
    logout(request)

def home(request):
    return render(request, 'home.html')

# accounts/views.py
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.full_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
            messages.success(request, f'Account created for {user.full_name}. Please log in.')
            return redirect('login')
    return render(request, 'accounts/signup.html')

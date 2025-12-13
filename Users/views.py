from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from hostel.models import Application, Allocation

def register(request):
    if request.method == "POST":
        username = request.POST['username'].strip()
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, "users/register.html", {'error':'Username exists'})
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        messages.success(request,"Account created")
        return redirect('login')
    return render(request,"users/register.html")

def login_view(request):
    if request.method == "POST":
        u=request.POST['username']; p=request.POST['password']
        user=authenticate(request, username=u, password=p)
        if user:
            login(request,user); return redirect('dashboard')
        return render(request,'users/login.html', {'error':'Invalid credentials'})
    return render(request,'users/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('dashboard')

@login_required
def dashboard(request):
    # show pending applications and allocation summary
    apps = Application.objects.filter(student=request.user).order_by('-created_at')[:5]
    allocation = getattr(request.user,'allocation', None)
    return render(request,'users/dashboard.html', {'applications':apps, 'allocation': allocation})
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *

def register(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if username and password:
            User.objects.create_user(
                username = username,
                password = password
            )
        return redirect('loginn')
    return render(request,'registration.html')




def loginn(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(
            request,
            username=data.get('username'),
            password=data.get('password')
        )
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')
    
    
    
@login_required
def logout_user(request):
    logout(request)
    return redirect('loginn')


def home(request):
    stadium = Field.objects.all()
    return render(request, 'home.html', {'stadium': stadium})




@login_required
def create_category(request):
    if request.method == 'POST':
        Category.objects.create(name=request.POST.get('name'))
        return redirect('home')
    return render(request, 'create_category.html')


@login_required
def create_stadium(request):
    if request.method == 'POST':
        Field.objects.create(
        name=request.POST.get('name')
        category=request.POST.get('category')
        desc=request.POST.get('desc')
        )
    

@login_required
def my_stadium(request):
    stadiums = Field.objects.filter(user=request.user)
    return render(request, 'my_stadium.html', {'stadiums': stadiums})












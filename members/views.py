
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.http import HttpResponse


# Create your views here.
# Create your views here.
def home(request):
    actions= request.GET.get('act')
    context={
        'action':actions,
    }
    return render(request,'home.html',context)

def choose_action(request):
    action=request.GET.get('action')
    context={
        'action':action,
    }
    return render(request, 'chose_action.html',context)

def Register(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        user_type= request.POST.get('user_type')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
        else:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user,user_type=user_type)
            
            
            messages.success(request, f'{user_type.capitalize()} registered successfully!')
            return redirect('/login')
    
    return render(request,'register.html')

# def Register_stud(request):
#     if request.method== 'POST':

#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Student already exist')
#         else:
#             user= User.objects.create_user(username=username, password=password)
#             user.profile.user_type='student'
#             user.profile.save()
#             messages.success(request, 'Student registered')
#             return redirect('members/')
#     return render (request, 'register.html')
        

def Login(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        selected_type = request.POST.get('user_type')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user,'profile') and user.profile.user_type==selected_type:
                login (request, user)
                messages.success(request, f"Logged in as {selected_type}")
                if selected_type=='student':
                    return redirect('/Students')
                else:
                    return redirect('/Teachers/teacher-dashboard')
            else:
                messages.error(request, "Invalid user type.")
        else: 
            messages.error(request, "Invalid credential")

    return render(request, 'login.html')


# def Login_stud(request):
#     if request.method== 'POST':
#         username= request.POST.get('username')
#         password= request.POST.get('password')
#         user = authenticate(request, ussername=username, password=password)
#         if user is not None and hasattr(user, 'profile') and user.profile.user_type=='student':
#             login (request, user)
#             return redirect ('student_dashboard')
#         else:
#             messages.error(request, 'invalid credential')
#     return render (request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('login')
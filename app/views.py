
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *

# Create your views here.
@login_required(login_url = 'login')
def home(request):

    return render(request,'app/home.html')

@login_required(login_url = 'login')
def send_message(request):

    return render(request,'app/send_message.html')

@login_required(login_url = 'login')
def send_channel_message(request):

    return render(request,'app/send_channel_message.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    user = authenticate(request, username=username,password=password)

                    if user is not None:
                        login(request, user)
                        return redirect('home')
                    else:
                        messages.info(request, 'Username or Password Is Incorrect')
                        return redirect('login')

        return render(request,'app/login.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + username)

                Person.objects.create(
				user = user,
                name = user.username
			)
                
                return redirect('login')
        context = {'form':form}
        return render(request,'app/register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')
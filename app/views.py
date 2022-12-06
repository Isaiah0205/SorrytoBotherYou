
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.core.mail import send_mass_mail
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse

# Create your views here.
@login_required(login_url = 'login')
def home(request):
    u = request.user
    if request.method == 'POST':
                    original_password = request.POST.get('original_password')
                    password_x1 = request.POST.get('password_x1')
                    password_x2 = request.POST.get('password_x2')
                    new_username = request.POST.get('new_username')
                    if original_password != None:
                        if u.check_password(original_password) == True:
                            if password_x1 == password_x2:
                                u.set_password(password_x1)
                                u.save()
                                messages.info(request, 'Password is updated.')
                                return redirect('home')

                            else:
                                messages.info(request, 'Passwords do not match.')
                                return redirect('home')
                        else:
                                messages.info(request, 'Passwords is incorrect.')
                                return redirect('home')
                    elif new_username != None:
                        p = Person.objects.get(user = u)
                        u.username = new_username
                        u.save()
                        p.name = new_username
                        p.save()
                        messages.info(request, 'Username has been changed.')
                        return redirect('login')
                        
                    else:
                        pass




    return render(request,'app/home.html')

@login_required(login_url = 'login')
def send_message(request):

    return render(request,'app/send_message.html')

@login_required(login_url = 'login')
def send_channel_message(request):

    return render(request,'app/Stats.html')

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


@login_required(login_url = 'login')
def send_email(request):
    form = SendEmailForm()
    if request.method == "POST":
        form = SendEmailForm(request.POST)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = settings.EMAIL_HOST_USER
        recipient_list = request.POST.get('recipient_list')
        if form.is_valid():
            send_mail(subject, message, from_email, [recipient_list], fail_silently=False)
            return redirect('/')
    context = {"form": form}
    return render(request, 'app/send_message.html', context)

def population_chart():
    labels = []
    data = []
    queryset = Email.objects.values('recipent_list').annotate(country_population=Sum('subject')).order_by('recipent_list')
    for entry in queryset:
        labels.append(entry['subject'])
        data.append(entry['recipent_list'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
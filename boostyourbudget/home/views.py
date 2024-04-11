from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'home/index.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('boost:boost')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('boost:boost')
            else:
                messages.info(request, 'Username or password is incorrect!')

        context = {}
        return render(request, 'home/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home:login')


def register(request):
    if request.user.is_authenticated:
        return redirect('boost:boost')
    
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('home:login')

        context = {'form': form}
        return render(request, 'home/register.html', context)
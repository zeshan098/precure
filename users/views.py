from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
 

# Create your views here.


def login(request): 
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('dashboard')
                 
            else:  
                messages.error(request,'username or password not correct')
                return redirect('login')    

    else:
        form = AuthenticationForm()

    return render(request, "admin/login.html", {'form': form})

def logout_request(request):
    logout(request) 
    return redirect("login")

@login_required(login_url='/users/login')
def dashboard(request):
    return render(request, 'admin/index.html',{}) 
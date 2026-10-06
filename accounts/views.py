from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if email and senha:
            user = authenticate(username=email, password=senha)
        else:
            messages.error(request, "Os campos devem ser preenchidos")
            return render(request, "accounts/home1.html")

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Senha ou Email invalido")
            return render(request, "accounts/home1.html")
    else:
        return render(request,"accounts/home1.html")

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url="/accounts/home1/")
def home(request):
    return render(request,"accounts/home.html")
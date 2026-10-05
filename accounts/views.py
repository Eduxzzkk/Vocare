from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def teste(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if email and senha:
            user = authenticate(username=email, password=senha)
        else:
            return HttpResponse("Os campos devem ser preenchidos")

        if user is not None:
            login(request, user)
            return HttpResponse("Login realizado com sucesso")
        else:
            return HttpResponse("Senha ou Email invalido")
    else:
        return render(request,"accounts/login.html")
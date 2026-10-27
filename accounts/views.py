from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


def lading_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "accounts/index.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not email or not password:
            messages.error(request, "Preencha todos os campos.")
            return redirect("lading_page")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "E-mail ou senha inválidos.")
        return redirect("lading_page")

    return redirect("lading_page")

def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "GET":
        return render(request, "accounts/cadastro/index.html")

    nome = request.POST.get("firstName", "").strip()
    sobrenome = request.POST.get("lastName", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "")
    termos = request.POST.get("terms")

    if not nome or not sobrenome or not email or not password:
        messages.error(request, "Preencha todos os campos.")
        return render(request, "accounts/cadastro/index.html")

    if not termos:
        messages.error(request, "Você precisa aceitar os termos.")
        return render(request, "accounts/cadastro/index.html")

    if CustomUser.objects.filter(email__iexact=email).exists():
        messages.error(request, "Este e-mail já está cadastrado.")
        return render(request, "accounts/cadastro/index.html")

    try:
        validate_password(password)
    except ValidationError as erro:
        for mensagem in erro.messages:
            messages.error(request, mensagem)
        return render(request, "accounts/cadastro/index.html")

    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        nome=f"{nome} {sobrenome}",
    )

    login(request, user)
    return redirect("home")


def logout_view(request):
    logout(request)
    return redirect("lading_page")


@login_required(login_url="login")
def home(request):
    return render(request, "accounts/home.html")
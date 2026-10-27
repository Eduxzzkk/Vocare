from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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


def logout_view(request):
    logout(request)
    return redirect("lading_page")


@login_required(login_url="login")
def home(request):
    return render(request, "accounts/home.html")
from django.urls import path
from . import views

urlpatterns = [
    path("", views.lading_page, name="lading_page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("cadastro/", views.cadastro_view, name="cadastro"),

]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_carreiras, name='lista_carreiras'),
    path('<int:carreira_id>/', views.detalhe_carreira, name='detalhe_carreira'),
]
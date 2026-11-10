from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_quizzes, name='lista_quizzes'),
    path('<int:quiz_id>/', views.detalhe_quiz, name='detalhe_quiz'),
    path('tentativas/<int:tentativa_id>/resultado/', views.resultado_tentativa, name='resultado_tentativa'),
]
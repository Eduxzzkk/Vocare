from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Alternativa, Tentativa, Resposta
from django.contrib.auth.decorators import login_required
from .services import calcular_perfil, ranking_carreiras
from collections import defaultdict

def lista_quizzes(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/lista_quizzes.html', {'quizzes': quizzes})

@login_required
def detalhe_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST':
        tentativa = Tentativa.objects.create(usuario=request.user, quiz=quiz)
        for pergunta in quiz.perguntas.all():
            alternativa_id = request.POST.get(f'pergunta_{pergunta.id}')
            if alternativa_id:
                alternativa = get_object_or_404(Alternativa, pk=alternativa_id, pergunta=pergunta)
                Resposta.objects.create(tentativa=tentativa, pergunta=pergunta, alternativa=alternativa)
        return redirect('resultado_tentativa', tentativa_id=tentativa.id)

    return render(request, 'quizzes/detalhe_quiz.html', {'quiz': quiz})

@login_required
def resultado_tentativa(request, tentativa_id):
    tentativa = get_object_or_404(Tentativa, pk=tentativa_id, usuario=request.user)
    perfil = calcular_perfil(tentativa)
    contexto = {
        'tentativa': tentativa,
        'perfil': sorted(perfil.items(), key=lambda par: par[1], reverse=True),
        'ranking': ranking_carreiras(perfil)[:3],
    }
    return render(request, 'quizzes/resultado.html', contexto)
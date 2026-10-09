from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Alternativa, Tentativa, Resposta
from django.contrib.auth.decorators import login_required
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

    pontos_por_carreira = defaultdict(int)
    for resposta in tentativa.respostas.all():
        for pontuacao in resposta.alternativa.pontuacoes.all():
            pontos_por_carreira[pontuacao.carreira] += pontuacao.pontos

    ranking = sorted(pontos_por_carreira.items(), key=lambda item: item[1], reverse=True)

    return render(request, 'quizzes/resultado.html', {'tentativa': tentativa, 'ranking': ranking[:3]})
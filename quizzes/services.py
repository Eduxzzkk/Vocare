# quizzes/services.py
from collections import defaultdict
from carreiras.models import Carreira
from .models import Tentativa


def pontos_da_tentativa(tentativa):
    """Devolve (obtidos, maximos): dois dicionários {dimensao: pontos}."""
    obtidos = defaultdict(int)
    for resposta in tentativa.respostas.all():
        for p in resposta.alternativa.pontuacoes.all():
            obtidos[p.dimensao] += p.pontos

    maximos = defaultdict(int)
    for pergunta in tentativa.quiz.perguntas.all():
        maior_na_pergunta = {}
        for alternativa in pergunta.alternativas.all():
            for p in alternativa.pontuacoes.all():
                atual = maior_na_pergunta.get(p.dimensao, 0)
                maior_na_pergunta[p.dimensao] = max(atual, p.pontos)
        for dimensao, maior in maior_na_pergunta.items():
            maximos[dimensao] += maior
    return obtidos, maximos


def normalizar(obtidos, maximos):
    """Converte pontos em proporção do máximo (0 a 1) por dimensão."""
    perfil = {}
    for dimensao, maximo in maximos.items():
        if maximo > 0:
            perfil[dimensao] = obtidos.get(dimensao, 0) / maximo
    return perfil


def calcular_perfil(tentativa):
    obtidos, maximos = pontos_da_tentativa(tentativa)
    return normalizar(obtidos, maximos)


def ultimas_tentativas(usuario):
    """A tentativa mais recente do usuário em cada quiz."""
    mais_recentes = {}
    for tentativa in Tentativa.objects.filter(usuario=usuario).order_by('data', 'id'):
        mais_recentes[tentativa.quiz_id] = tentativa
    return list(mais_recentes.values())


def calcular_perfil_acumulado(tentativas):
    obtidos_total = defaultdict(int)
    maximos_total = defaultdict(int)
    for tentativa in tentativas:
        obtidos, maximos = pontos_da_tentativa(tentativa)
        for dimensao, pontos in obtidos.items():
            obtidos_total[dimensao] += pontos
        for dimensao, pontos in maximos.items():
            maximos_total[dimensao] += pontos
    return normalizar(obtidos_total, maximos_total)

def ranking_carreiras(perfil):
    """Devolve [(carreira, afinidade)] ordenado do maior para o menor."""
    resultado = []
    for carreira in Carreira.objects.all():
        soma_ponderada = 0
        soma_pesos = 0
        for item in carreira.perfil.all():
            if item.dimensao in perfil:
                soma_ponderada += perfil[item.dimensao] * item.peso
                soma_pesos += item.peso
        if soma_pesos > 0:
            resultado.append((carreira, soma_ponderada / soma_pesos))
    resultado.sort(key=lambda par: par[1], reverse=True)
    return resultado


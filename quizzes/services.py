from collections import defaultdict
from carreiras.models import Carreira


def calcular_perfil(tentativa):
    """Devolve {dimensao: valor de 0 a 1} para uma tentativa."""
    # 1) pontos que o usuário obteve em cada dimensão
    obtidos = defaultdict(int)
    for resposta in tentativa.respostas.all():
        for p in resposta.alternativa.pontuacoes.all():
            obtidos[p.dimensao] += p.pontos

    # 2) máximo que era possível obter em cada dimensão neste quiz
    maximos = defaultdict(int)
    for pergunta in tentativa.quiz.perguntas.all():
        maior_na_pergunta = {}
        for alternativa in pergunta.alternativas.all():
            for p in alternativa.pontuacoes.all():
                atual = maior_na_pergunta.get(p.dimensao, 0)
                maior_na_pergunta[p.dimensao] = max(atual, p.pontos)
        for dimensao, maior in maior_na_pergunta.items():
            maximos[dimensao] += maior

    # 3) normalização: obtido / máximo
    perfil = {}
    for dimensao, maximo in maximos.items():
        if maximo > 0:
            perfil[dimensao] = obtidos[dimensao] / maximo
    return perfil


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
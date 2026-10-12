from django.db import models
from django.conf import settings

class Quiz(models.Model):
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.titulo


class DimensaoVocacional(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Pergunta(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto


class Alternativa(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='alternativas')
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto

class AlternativaDimensao(models.Model):
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE, related_name='pontuacoes')
    dimensao = models.ForeignKey(DimensaoVocacional, on_delete=models.CASCADE, related_name='pontuacoes_alternativas')
    pontos = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['alternativa', 'dimensao'], name='pontuacao_unica_alternativa_dimensao'),
        ]

    def __str__(self):
        return f"{self.alternativa.texto[:30]} -> {self.dimensao}: {self.pontos} pontos"


class Tentativa(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tentativas')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='tentativas')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.quiz}"


class Resposta(models.Model):
    tentativa = models.ForeignKey(Tentativa, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='respostas')
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE, related_name='respostas')

    def __str__(self):
        return f"{self.tentativa}: P. {self.pergunta.texto[:100]} A. {self.alternativa.texto[:100]}"
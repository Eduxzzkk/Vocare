from django.db import models
from django.conf import settings
from quizzes.models import DimensaoVocacional
from django.core.validators import MinValueValidator

class Carreira(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    dimensoes = models.ManyToManyField(DimensaoVocacional, through='PerfilCarreira', related_name='carreiras')

    def __str__(self):
        return self.nome


class PerfilCarreira(models.Model):
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE, related_name='perfil')
    dimensao = models.ForeignKey(DimensaoVocacional, on_delete=models.CASCADE, related_name='perfis_carreira')
    peso = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['carreira', 'dimensao'], name='perfil_unico_carreira_dimensao'),
        ]

    def __str__(self):
        return f"{self.carreira} - {self.dimensao}: peso {self.peso}"
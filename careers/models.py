from django.db import models

# Create your models here.

class Carreira(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField() # Aqui eu removi o "blank=true" para que a descricao seja algo obrigatorio. Se achar necessario deixar o campo blank true pode deixar!

    def __str__(self):
        return self.nome
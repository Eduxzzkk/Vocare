from django.contrib import admin
from .models import Quiz, Pergunta, Alternativa, PontuacaoCarreira, Tentativa, Resposta

admin.site.register(Quiz)
admin.site.register(Pergunta)
admin.site.register(Alternativa)
admin.site.register(PontuacaoCarreira)
admin.site.register(Tentativa)
admin.site.register(Resposta)
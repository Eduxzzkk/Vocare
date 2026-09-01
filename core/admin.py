from django.contrib import admin
from .models import Carreira, Quiz, Pergunta, Alternativa, PontuacaoCarreira, Tentativa, Resposta
from accounts.models import CustomUser

admin.site.register(Carreira)
admin.site.register(Quiz)
admin.site.register(Pergunta)
admin.site.register(Alternativa)
admin.site.register(PontuacaoCarreira)
admin.site.register(Tentativa)
admin.site.register(Resposta)
admin.site.register(CustomUser)
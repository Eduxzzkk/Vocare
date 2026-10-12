from django.contrib import admin
from .models import Quiz, Pergunta, DimensaoVocacional, Alternativa, AlternativaDimensao, Tentativa, Resposta

admin.site.register(Quiz)
admin.site.register(Pergunta)
admin.site.register(Alternativa)
admin.site.register(DimensaoVocacional)
admin.site.register(AlternativaDimensao)
admin.site.register(Tentativa)
admin.site.register(Resposta)
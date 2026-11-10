from django.shortcuts import render, get_object_or_404
from .models import Carreira

def lista_carreiras(request):
    carreiras = Carreira.objects.all()
    return render(request, 'carreiras/lista_carreiras.html', {'carreiras': carreiras})

def detalhe_carreira(request, carreira_id):
    carreira = get_object_or_404(Carreira, pk=carreira_id)
    return render(request, 'carreiras/detalhe_carreira.html', {'carreira': carreira})

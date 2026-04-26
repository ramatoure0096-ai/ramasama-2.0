from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import json
from django.shortcuts import render
from django.db.models import Sum
from .models import Vente

def log_in(request):
    if request.method == 'POST':
        f = AuthenticationForm(data=request.POST)
        if f.is_valid():
            u = f.get_user()
            login(request, u)
            messages.success(request, "Bienvenue !")
            return redirect('login')
    else:
        f = AuthenticationForm()
    return render(request, 'ramasama/login.html', {'form': f}) 

def log_out(request):
    logout(request)
    messages.info(request, "Bye !")
    return redirect('login')

# Create your views here.
def dashboard_view(request):
    # 1. Calcul des KPIs pour les cartes colorées
    total_ca = Vente.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    nb_ventes = Vente.objects.count()
    progression = 75  # Exemple statique pour l'instant
    
    # 2. Préparation des données pour Chart.js
    # On récupère par exemple les 7 dernières ventes
    dernieres_ventes = Vente.objects.order_by('-date')[:7]
    
    # On crée les listes Python
    labels = [v.date.strftime("%d/%m") for v in dernieres_ventes]
    data_ventes = [float(v.montant) for v in dernieres_ventes]
    
    # IMPORTANT : On inverse pour avoir l'ordre chronologique (gauche à droite)
    labels.reverse()
    data_ventes.reverse()

    context = {
        'total_ca': total_ca,
        'nb_ventes': nb_ventes,
        'progression': progression,
        'labels': labels,        # Sera lu par {{ labels|safe }}
        'data_ventes': data_ventes, # Sera lu par {{ data_ventes|safe }}
    }
    
    return render(request, 'dashboard/index.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.core.mail import send_mail # Indispensable pour tes notifications email
from .models import Vente
from .forms import VenteForm 

# --- AUTHENTIFICATION ---

def log_in(request):
    if request.method == 'POST':
        f = AuthenticationForm(data=request.POST)
        if f.is_valid():
            u = f.get_user()
            login(request, u)
            messages.success(request, f"Bienvenue {u.username} ! (●'◡'●)")
            return redirect('dashboard') 
    else:
        f = AuthenticationForm()
    # Note : assure-toi que le fichier est bien dans templates/ramasama/login.html
    return render(request, 'ramasama/login.html', {'form': f}) 

def log_out(request):
    logout(request)
    messages.info(request, "Déconnexion réussie. À bientôt ! (┬┬﹏┬┬)")
    return redirect('login')

# --- DASHBOARD & STATS ---

@login_required(login_url='login')
def dashboard_view(request):
    total_ca = Vente.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    nb_ventes = Vente.objects.count()
    progression = 75  # À dynamiser plus tard avec les Objectifs
    
    dernieres_ventes = Vente.objects.order_by('-date')[:7]
    
    labels = [v.date.strftime("%d/%m") for v in dernieres_ventes]
    data_ventes = [float(v.montant) for v in dernieres_ventes]
    
    labels.reverse()
    data_ventes.reverse()

    context = {
        'total_ca': total_ca,
        'nb_ventes': nb_ventes,
        'progression': progression,
        'labels': labels,
        'data_ventes': data_ventes,
    }
    return render(request, 'dashboard/index.html', context)

# --- GESTION DES VENTES & NOTIFICATIONS ---

@login_required(login_url='login')
def ajouter_vente(request):
    if request.method == "POST":
        form = VenteForm(request.POST)
        if form.is_valid():
            # Sauvegarde de la vente
            vente = form.save()
            
            # 1. Notification In-App
            messages.success(request, "La vente a été enregistrée avec succès !")
            
            # 2. Notification Email (Seulement si gros montant > 1.000.000)
            if vente.montant > 1000000:
                send_mail(
                    'Alerte : Grosse Vente Réalisée',
                    f'Une vente de {vente.montant} FCFA vient d\'être effectuée par {vente.vendeur}.',
                    'system@ramasama.ga',
                    ['responsable@entreprise.ga'],
                    fail_silently=True,
                )
            
            return redirect('liste_ventes')
        else:
            messages.error(request, "Erreur lors de l'enregistrement.")
    else:
        form = VenteForm()
    
    return render(request, 'dashboard/liste_formulaire.html', {'form': form})
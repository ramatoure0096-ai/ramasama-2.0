from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from django.core.mail import send_mail
from .models import Vente, Produit, Vendeur
from .forms import VenteForm

# --- FONCTIONS DE PROTECTION DES RÔLES ---

def est_directeur(user):
    return user.groups.filter(name='Directeur').exists() or user.is_superuser

def est_vendeur_ou_responsable(user):
    return user.groups.filter(name__in=['Vendeur', 'Responsable Commercial']).exists() or user.is_superuser

# --- AUTHENTIFICATION ---

def log_in(request):
    if request.method == 'POST':
        f = AuthenticationForm(data=request.POST)
        if f.is_valid():
            u = f.get_user()
            login(request, u)
            messages.success(request, f"Bienvenue {u.username} ! ✨ (Rôle: {u.groups.first()})")
            return redirect('dashboard')
    else:
        f = AuthenticationForm()
    return render(request, 'ramasama/login.html', {'form': f})

def log_out(request):
    logout(request)
    messages.info(request, "Déconnexion réussie. À bientôt ! 👋")
    return redirect('login')

# --- DASHBOARD & ANALYTIQUE ---

@login_required(login_url='login')
def dashboard_view(request):
    # KPIs pour les indicateurs clés
    total_ca = Vente.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    nb_ventes = Vente.objects.count()
    
    # Données pour le graphique Chart.js (7 dernières ventes)
    dernieres_ventes = Vente.objects.order_by('-date')[:7]
    labels = [v.date.strftime("%d/%m") for v in dernieres_ventes]
    data_ventes = [float(v.montant) for v in dernieres_ventes]
    
    labels.reverse()
    data_ventes.reverse()

    context = {
        'total_ca': total_ca,
        'nb_ventes': nb_ventes,
        'labels': labels,
        'data_ventes': data_ventes,
        'est_directeur': est_directeur(request.user), # Pour afficher/masquer l'export PDF
    }
    return render(request, 'dashboard/index.html', context)

# --- GESTION DES VENTES (CRUD + NOTIFICATIONS) ---

@login_required(login_url='login')
def liste_ventes(request):
    # Récupération de toutes les ventes pour le tableau
    ventes = Vente.objects.all().order_by('-date')
    return render(request, 'dashboard/liste_ventes.html', {'ventes': ventes})

@login_required(login_url='login')
@user_passes_test(est_vendeur_ou_responsable) # Sécurité : seul le staff commercial accède
def ajouter_vente(request):
    if request.method == "POST":
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save()
            
            # 1. Notification In-App (Framework de messages)
            messages.success(request, f"Vente de {vente.produit.nom_prod} enregistrée avec succès !")
            
            # 2. Notification Email (Django Email Backend)
            # Alerte si montant > 1.000.000 FCFA
            if vente.montant > 1000000:
                send_mail(
                    'ALERTE : Vente Exceptionnelle',
                    f'Une vente majeure de {vente.montant} FCFA a été réalisée par {vente.vendeur.nom_vendeur}.',
                    'system@ramasama.ga',
                    ['directeur@entreprise.ga', 'responsable@entreprise.ga'],
                    fail_silently=True,
                )
            
            return redirect('liste_ventes')
        else:
            messages.error(request, "Erreur lors de la validation du formulaire.")
    else:
        form = VenteForm()
    
    return render(request, 'dashboard/liste_formulaire.html', {'form': form})

# --- EXPORTATION (Bouton spécial Directeur) ---

@login_required(login_url='login')
@user_passes_test(est_directeur)
def export_confirm(request):
    return render(request, 'dashboard/export_confirm.html')
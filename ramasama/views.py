import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import HttpResponse
from .models import Vente, Produit, Vendeur

# PDF Imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm

# --- AUTH ---
def log_in(request):
    if request.method == 'POST':
        f = AuthenticationForm(data=request.POST)
        if f.is_valid():
            u = f.get_user()
            login(request, u)
            return redirect('dashboard_view') 
    else:
        f = AuthenticationForm()
    return render(request, 'ramasama/login.html', {'form': f})

def log_out(request):
    logout(request)
    return redirect('login')

# --- DASHBOARD + GRAPHES ---
@login_required(login_url='login')
def dashboard_view(request):
    ventes_qs = Vente.objects.all()
    
    # Sécurité Vendeur : ne voit que ses ventes
    if not request.user.is_superuser:
        ventes_qs = ventes_qs.filter(vendeur__prenom_vendeur__icontains=request.user.username)

    total_ca = ventes_qs.aggregate(Sum('montant'))['montant__sum'] or 0
    nb_ventes = ventes_qs.count()
    panier_moyen = total_ca / nb_ventes if nb_ventes > 0 else 0
    
    # DONNÉES DU GRAPHE
    dernieres_ventes = ventes_qs.order_by('-date')[:10]
    labels = [v.date.strftime("%d/%m") for v in dernieres_ventes]
    data_ventes = [float(v.montant) for v in dernieres_ventes]
    
    # On inverse pour avoir l'ordre chrono (gauche -> droite)
    labels.reverse()
    data_ventes.reverse()

    context = {
        'total_ca': total_ca,
        'nb_ventes': nb_ventes,
        'panier_moyen': panier_moyen,
        'is_admin': request.user.is_superuser,
        'produits': Produit.objects.all().order_by('-id_prod'),
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data_ventes),
    }
    return render(request, 'dashboard/index.html', context)

# --- VENTES ---
@login_required(login_url='login')
def vente_list_view(request):
    if request.user.is_superuser:
        ventes = Vente.objects.all().order_by('-date')
    else:
        ventes = Vente.objects.filter(vendeur__prenom_vendeur__icontains=request.user.username).order_by('-date')
    return render(request, 'dashboard/liste_ventes.html', {'ventes': ventes})

@login_required(login_url='login')
def vente_create_view(request):
    if request.method == 'POST':
        p = get_object_or_404(Produit, id_prod=request.POST.get('produit'))
        v = get_object_or_404(Vendeur, id_vendeur=request.POST.get('vendeur'))
        qte = int(request.POST.get('quantite', 1))
        Vente.objects.create(produit=p, vendeur=v, quantite=qte, montant=(p.prix * qte))
        messages.success(request, "Vente enregistrée ! 💰")
        return redirect('vente_list')
    
    vendeurs = Vendeur.objects.all() if request.user.is_superuser else Vendeur.objects.filter(prenom_vendeur__icontains=request.user.username)
    return render(request, 'dashboard/liste_formulaire.html', {'produits': Produit.objects.all(), 'vendeurs': vendeurs})

@login_required(login_url='login')
def vente_delete_view(request, pk):
    vente = get_object_or_404(Vente, id_vente=pk)
    if not request.user.is_superuser and vente.vendeur.prenom_vendeur.lower() != request.user.username.lower():
        return redirect('vente_list')
    if request.method == 'POST':
        vente.delete()
        return redirect('vente_list')
    return render(request, 'dashboard/confirmer_suppression.html', {'vente': vente, 'type': 'vente'})

# --- PDF ---
@login_required(login_url='login')
def export_vente_pdf(request, pk):
    vente = get_object_or_404(Vente, id_vente=pk)
    response = HttpResponse(content_type='application/pdf')
    p = canvas.Canvas(response, pagesize=A6)
    p.drawString(15*mm, 100*mm, f"RECU RAMASAMA - {vente.id_vente}")
    p.drawString(15*mm, 90*mm, f"Total: {vente.montant} FCFA")
    p.showPage(); p.save()
    return response

# --- PRODUITS (ADMIN) ---
@login_required(login_url='login')
def produit_create_view(request):
    if not request.user.is_superuser: return redirect('dashboard_view')
    if request.method == 'POST':
        Produit.objects.create(nom_prod=request.POST.get('nom'), categorie_prod=request.POST.get('type'), prix=request.POST.get('prix'))
        return redirect('dashboard_view')
    return render(request, 'dashboard/ajouter_produit.html')

@login_required(login_url='login')
def produit_edit_view(request, pk):
    if not request.user.is_superuser: return redirect('dashboard_view')
    p = get_object_or_404(Produit, id_prod=pk)
    if request.method == 'POST':
        p.nom_prod = request.POST.get('nom'); p.categorie_prod = request.POST.get('type'); p.prix = request.POST.get('prix')
        p.save(); return redirect('dashboard_view')
    return render(request, 'dashboard/modifier_produit.html', {'produit': p})

@login_required(login_url='login')
def produit_delete_view(request, pk):
    if not request.user.is_superuser: return redirect('dashboard_view')
    p = get_object_or_404(Produit, id_prod=pk)
    if request.method == 'POST':
        p.delete(); return redirect('dashboard_view')
    return render(request, 'dashboard/confirmer_suppression.html', {'produit': p, 'type': 'produit'})
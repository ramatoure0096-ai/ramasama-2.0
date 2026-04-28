import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from .models import Vente, Produit, Vendeur

# --- AUTH ---
def log_in(request):
    if request.method == 'POST':
        f = AuthenticationForm(data=request.POST)
        if f.is_valid():
            login(request, f.get_user())
            return redirect('dashboard_view') 
    else:
        f = AuthenticationForm()
    return render(request, 'ramasama/login.html', {'form': f})

def log_out(request):
    logout(request)
    return redirect('login')

# --- DASHBOARD (GRAPHE OK 📊) ---
@login_required(login_url='login')
def dashboard_view(request):
    is_admin = request.user.is_superuser
    if is_admin:
        ventes_qs = Vente.objects.all()
        role = "Responsable Commercial"
    else:
        ventes_qs = Vente.objects.filter(vendeur__prenom_vendeur__icontains=request.user.username)
        role = "Vendeur Certifié"

    # Données Graphe
    dernieres_ventes = ventes_qs.order_by('-date')[:10]
    labels = [v.date.strftime("%d/%m") for v in dernieres_ventes]
    data_ventes = [float(v.montant) for v in dernieres_ventes]
    labels.reverse()
    data_ventes.reverse()

    context = {
        'total_ca': ventes_qs.aggregate(Sum('montant'))['montant__sum'] or 0,
        'nb_ventes': ventes_qs.count(),
        'role': role,
        'is_admin': is_admin,
        'produits': Produit.objects.all().order_by('-id_prod'),
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data_ventes),
    }
    return render(request, 'dashboard/index.html', context)

# --- REÇU SANS FICHIER HTML (ANTI-ERREUR 🧾) ---
@login_required(login_url='login')
def recu_vente_view(request, pk):
    vente = get_object_or_404(Vente, id_vente=pk)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8"><title>Recu #{vente.id_vente}</title>
        <style>
            @page {{ size: 80mm auto; margin: 0; }}
            body {{ font-family: monospace; padding: 20px; text-align: center; background: #eee; }}
            .ticket {{ width: 70mm; background: white; margin: 0 auto; padding: 10px; border: 1px solid #ddd; text-align: left; }}
            .header {{ text-align: center; border-bottom: 1px dashed #000; }}
            .total {{ font-size: 1.2em; font-weight: bold; margin-top: 10px; text-align: right; }}
            button {{ padding: 10px; background: black; color: white; border: none; cursor: pointer; width: 100%; border-radius: 5px; }}
            @media print {{ .no-print {{ display: none; }} body {{ background: white; padding: 0; }} .ticket {{ border: none; }} }}
        </style>
    </head>
    <body>
        <div class="no-print" style="margin-bottom:20px;">
            <button onclick="window.print()">🖨️ IMPRIMER / SAUVEGARDER PDF</button>
            <p><a href="/ventes/">← Retour</a></p>
        </div>
        <div class="ticket">
            <div class="header"><h2>RAMASAMA</h2><p>Ticket #{vente.id_vente}</p></div>
            <p><b>Date:</b> {vente.date.strftime('%d/%m/%Y %H:%M')}</p>
            <p><b>Vendeur:</b> {vente.vendeur.prenom_vendeur}</p>
            <hr style="border-top: 1px dashed #000;">
            <p>{vente.produit.nom_prod} (x{vente.quantite})</p>
            <div class="total">TOTAL: {vente.montant} FCFA</div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

# --- VENTES ---
@login_required(login_url='login')
def vente_list_view(request):
    if request.user.is_superuser:
        ventes = Vente.objects.all().order_by('-date')
    else:
        ventes = Vente.objects.filter(vendeur__prenom_vendeur__icontains=request.user.username).order_by('-date')
    return render(request, 'dashboard/liste_ventes.html', {'ventes': ventes})

@login_required(login_url='login')
def vente_delete_view(request, pk):
    get_object_or_404(Vente, id_vente=pk).delete()
    return redirect('vente_list')

@login_required(login_url='login')
def vente_create_view(request):
    if request.method == 'POST':
        p = get_object_or_404(Produit, id_prod=request.POST.get('produit'))
        v = Vendeur.objects.filter(prenom_vendeur__icontains=request.user.username).first() if not request.user.is_superuser else get_object_or_404(Vendeur, id_vendeur=request.POST.get('vendeur'))
        Vente.objects.create(produit=p, vendeur=v, quantite=int(request.POST.get('quantite', 1)), montant=(p.prix * int(request.POST.get('quantite', 1))))
        return redirect('vente_list')
    vendeurs = Vendeur.objects.all() if request.user.is_superuser else Vendeur.objects.filter(prenom_vendeur__icontains=request.user.username)
    return render(request, 'dashboard/liste_formulaire.html', {'produits': Produit.objects.all(), 'vendeurs': vendeurs})

# --- PRODUITS ---
@login_required(login_url='login')
def produit_create_view(request):
    if not request.user.is_superuser: return redirect('dashboard_view')
    if request.method == 'POST':
        Produit.objects.create(nom_prod=request.POST.get('nom'), prix=request.POST.get('prix'))
        return redirect('dashboard_view')
    return render(request, 'dashboard/ajouter_produit.html')

@login_required(login_url='login')
def produit_edit_view(request, pk):
    if not request.user.is_superuser: return redirect('dashboard_view')
    p = get_object_or_404(Produit, id_prod=pk)
    if request.method == 'POST':
        p.nom_prod = request.POST.get('nom'); p.prix = request.POST.get('prix'); p.save()
        return redirect('dashboard_view')
    return render(request, 'dashboard/modifier_produit.html', {'produit': p})
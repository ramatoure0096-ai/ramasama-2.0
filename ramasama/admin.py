from django.contrib import admin
from .models import Produit, Vendeur, Vente

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    # Ajout de 'prix' dans l'affichage, c'est plus pratique pour le DG ! 💰
    list_display = ('id_prod', 'nom_prod', 'categorie_prod', 'prix')
    search_fields = ('nom_prod',)

@admin.register(Vendeur)
class VendeurAdmin(admin.ModelAdmin):
    # J'ai retiré 'zone_vendeur' car il n'est pas dans ton models.py
    list_display = ('id_vendeur', 'prenom_vendeur', 'nom_vendeur')
    search_fields = ('nom_vendeur', 'prenom_vendeur')

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ('id_vente', 'produit', 'vendeur', 'quantite', 'montant', 'date')
    list_filter = ('date', 'vendeur', 'produit')
    date_hierarchy = 'date'
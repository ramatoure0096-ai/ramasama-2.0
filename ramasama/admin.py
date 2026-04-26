from django.contrib import admin
from .models import Produit, Vendeur, Objectif, Vente

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('id_prod', 'nom_prod', 'categorie_prod')
    search_fields = ('nom_prod',)

@admin.register(Vendeur)
class VendeurAdmin(admin.ModelAdmin):
    list_display = ('id_vendeur', 'prenom_vendeur', 'nom_vendeur', 'zone_vendeur')
    search_fields = ('nom_vendeur', 'prenom_vendeur')

@admin.register(Objectif)
class ObjectifAdmin(admin.ModelAdmin):
    list_display = ('id_objectif', 'id_vendeur', 'mois', 'montant_cible')
    list_filter = ('mois',)

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ('id_vente', 'produit', 'vendeur', 'quantite', 'montant', 'date')
    list_filter = ('date', 'vendeur', 'produit')
    date_hierarchy = 'date' # Ça ajoute une barre de navigation par date en haut, très chic !
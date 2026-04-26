from django.db import models

class Produit(models.Model):
    id_prod = models.AutoField(primary_key=True)
    nom_prod = models.CharField(max_length=100)
    categorie_prod = models.CharField(max_length=100)  # corrigé sans accent
    
    def __str__(self):
        return self.nom_prod
class Vendeur(models.Model):
    id_vendeur = models.AutoField(primary_key=True)
    nom_vendeur = models.CharField(max_length=100)
    prenom_vendeur = models.CharField(max_length=100)
    zone_vendeur = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.prenom_vendeur} {self.nom_vendeur}"
class Objectif(models.Model):
    id_objectif = models.AutoField(primary_key=True)
    id_vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)
    mois = models.CharField(max_length=20)
    montant_cible = models.FloatField()

    def __str__(self):
        return f"Objectif {self.id_objectif} - {self.id_vendeur}"

class Vente(models.Model):
    id_vente = models.AutoField(primary_key=True)
    # Relation vers Produit : si on supprime un produit, on garde la trace de la vente (SET_NULL)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, related_name='ventes')
    # Relation vers Vendeur
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE, related_name='ventes')
    
    quantite = models.IntegerField(default=1)
    montant = models.DecimalField(max_digits=12, decimal_places=2) # Préférable au Float pour la monnaie (FCFA)
    date = models.DateTimeField(auto_now_add=True) # Enregistre la date et l'heure automatiquement

    def __str__(self):
        return f"Vente {self.id_vente} - {self.produit.nom_prod if self.produit else 'Inconnu'}"

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
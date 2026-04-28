from django.db import models

class Vendeur(models.Model):
    id_vendeur = models.AutoField(primary_key=True)
    nom_vendeur = models.CharField(max_length=100)
    prenom_vendeur = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom_vendeur} {self.nom_vendeur}"

class Produit(models.Model):
    id_prod = models.AutoField(primary_key=True)
    nom_prod = models.CharField(max_length=100)
    categorie_prod = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.nom_prod

class Vente(models.Model):
    id_vente = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
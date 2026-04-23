from django.db import models

class Produit(models.Model):
    id_prod = models.AutoField(primary_key=True)
    nom_prod = models.CharField(max_length=100)
    categorie_prod = models.CharField(max_length=100)  # corrigé sans accent

class Vendeur(models.Model):
    id_vendeur = models.AutoField(primary_key=True)
    nom_vendeur = models.CharField(max_length=100)
    prenom_vendeur = models.CharField(max_length=100)
    zone_vendeur = models.CharField(max_length=200)

class Objectif(models.Model):
    id_objectif = models.AutoField(primary_key=True)
    id_vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)
    mois = models.CharField(max_length=20)
    montant_cible = models.FloatField()

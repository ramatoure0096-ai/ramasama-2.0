from django.db import models

# Create your models here 
class Produit(models.Model):
    id_prod        = models.AutoField(primary_key=True)
    nom_prod       = models.CharField(max_length=100)
    catégorie_prod = models.CharField(max_length=100)

class Vendeur(models.Model):
    id_vendeur     = models.AutoField(primary_key=True)
    nom_vendeur    = models.CharField(max_length=100)
    prenom_vendeur = models.CharField(max_length=100)
    zone_vendeur = models.CharField(max_length=200)

class Objectif(models.Model):
    id_objectif = models.AutoField(primary_key=True)
    id_vendeur = models.ForeignKey(Vendeur)
    mois =models.CharField(max_length=20)
    montant_cible = models.FloatField()

class Vente(models.Model):
    id_vente = models.AutoField(primary_key=True)
    id_vendeur = models.ForeignKey(Vendeur)
    id_prod = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    montant = models.FloatField()
    date = models.DateFields()
    

# forms.py
from django import forms
from .models import Vente

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        #on liste nos champs de la table vente
        fields = ['produit', 'vendeur', 'quantite', 'montant', 'date']
        #Ajout des classes ccs de boostrap pour le style rama je suis nul en design oh
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'vendeur': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 10'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
def clean_quantite(self):
        quantite = self.cleaned_data.get('quantite')
        if quantite <= 0:
            raise forms.ValidationError("La quantité doit être supérieure à zéro.")
        return quantite
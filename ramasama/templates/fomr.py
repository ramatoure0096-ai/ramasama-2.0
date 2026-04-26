# forms.py
from django import forms
from .models import Vente

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['produit', 'vendeur', 'quantite', 'montant', 'date']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'vendeur': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 10'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
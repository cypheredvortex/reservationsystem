from django import forms
from .models import Maison

class MaisonForm(forms.ModelForm):
    class Meta:
        model = Maison
        fields = ['titre', 'description', 'adresse', 'prix_par_nuit', 'disponible', 'image']
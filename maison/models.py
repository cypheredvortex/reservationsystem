from django.db import models
from user.models import UserProfile

class Maison(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    adresse = models.CharField(max_length=255)
    prix_par_nuit = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    proprietaire = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'proprietaire'})

    def __str__(self):
        return self.titre



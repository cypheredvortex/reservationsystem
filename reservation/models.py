from django.db import models
from user.models import UserProfile
from maison.models import Maison

class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmée', 'Confirmée'),
        ('annulée', 'Annulée'),
    ]
    utilisateur = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    maison = models.ForeignKey(Maison, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
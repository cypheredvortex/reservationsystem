from django.db import models
from user.models import UserProfile
from maison.models import Maison
from reservation.models import Reservation

class Paiement(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=50, choices=[
        ('carte', 'Credit Card'),
        ('virement', 'Bank Transfer'),
        ('paypal', 'PayPal')
    ])
    statut_paiement = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ])

    class Meta:
        db_table = 'paiement_paiement'
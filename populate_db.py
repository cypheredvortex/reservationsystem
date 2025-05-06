import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservationsystem.settings')
django.setup()

from django.contrib.auth.models import User
from user.models import UserProfile
from maison.models import Maison
from reservation.models import Reservation
from paiement.models import Paiement
from django.utils import timezone
from datetime import timedelta
from faker import Faker
import random

# Set up Django environment


fake = Faker()

def create_users(num_owners=3, num_clients=5):
    owners = []
    clients = []
    
    # Create property owners
    for i in range(num_owners):
        username = f"owner{i+1}"
        email = fake.email()
        user = User.objects.create_user(username, email, 'password123')
        profile = UserProfile.objects.create(user=user, role='proprietaire')
        owners.append(profile)
        print(f"Created owner: {username}")

    # Create clients
    for i in range(num_clients):
        username = f"client{i+1}"
        email = fake.email()
        user = User.objects.create_user(username, email, 'password123')
        profile = UserProfile.objects.create(user=user, role='client')
        clients.append(profile)
        print(f"Created client: {username}")
    
    return owners, clients

def create_houses(owners, num_houses=10):
    houses = []
    house_types = ['Villa', 'Apartment', 'Cottage', 'Beach House', 'Mountain Cabin', 'Penthouse']
    
    for _ in range(num_houses):
        house_type = random.choice(house_types)
        title = f"{fake.city()} {house_type}"
        
        house = Maison.objects.create(
            titre=title,
            description=fake.paragraph(),
            adresse=fake.address(),
            prix_par_nuit=random.randint(50, 500),
            disponible=random.choice([True, True, False]),  # 2/3 chance of being available
            proprietaire=random.choice(owners)
        )
        houses.append(house)
        print(f"Created house: {title}")
    
    return houses

def create_reservations(clients, houses, num_reservations=15):
    for _ in range(num_reservations):
        # Random dates within next 60 days
        start_date = timezone.now().date() + timedelta(days=random.randint(1, 30))
        duration = random.randint(1, 10)
        end_date = start_date + timedelta(days=duration)
        
        reservation = Reservation.objects.create(
            utilisateur=random.choice(clients),
            maison=random.choice(houses),
            date_debut=start_date,
            date_fin=end_date,
            statut=random.choice(['en_attente', 'confirmée', 'annulée'])
        )
        
        if reservation.statut == 'confirmée':
            Paiement.objects.create(
                reservation=reservation,
                montant=reservation.maison.prix_par_nuit * duration,
                mode_paiement=random.choice(['carte', 'paypal', 'virement']),
                statut_paiement=random.choice(['en_attente', 'payé', 'remboursé'])
            )
        print(f"Created reservation for {reservation.maison.titre}")

if __name__ == '__main__':
    print("Creating random sample data...")
    owners, clients = create_users()
    houses = create_houses(owners)
    create_reservations(clients, houses)
    print("Random sample data created successfully!")
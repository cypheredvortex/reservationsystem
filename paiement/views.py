from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from .models import Paiement
from reservation.models import Reservation

# Create your views here.
@login_required
def process_payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    
    # Check if payment already exists
    existing_payment = Paiement.objects.filter(reservation_id=reservation_id).first()
    if existing_payment:
        messages.error(request, 'A payment already exists for this reservation.')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        try:
            payment = Paiement.objects.create(
                reservation=reservation,
                montant=reservation.maison.prix_par_nuit,
                date_paiement=timezone.now(),
                mode_paiement=request.POST.get('mode_paiement', 'carte'),
                statut_paiement='completed'
            )
            messages.success(request, 'Payment processed successfully!')
            return redirect('payment_confirmation', payment_id=payment.id)
        except IntegrityError:
            messages.error(request, 'This reservation has already been paid for.')
            return redirect('my_reservations')
    
    return render(request, 'paiement/process_payment.html', {
        'reservation': reservation
    })

@login_required
def payment_history(request):
    payments = Paiement.objects.filter(reservation__utilisateur__user=request.user)
    return render(request, 'paiement/history.html', {'payments': payments})

@login_required
def payment_confirmation(request, payment_id):
    payment = get_object_or_404(Paiement, id=payment_id)
    return render(request, 'paiement/payment_confirmation.html', {'payment': payment})

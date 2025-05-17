from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reservation
from maison.models import Maison
from .forms import ReservationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReservationForm
from .models import Reservation
from maison.models import Maison
from messaging.forms import MessageForm

@login_required
def create_reservation(request, house_id):
    house = get_object_or_404(Maison, id=house_id)

    if request.method == 'POST':
        # on bind les deux forms sur POST
        res_form     = ReservationForm(request.POST)
        message_form = MessageForm(request.POST)

        # 1️⃣ Gestion du clic « Contact Owner »
        if 'contact' in request.POST:
            if message_form.is_valid():
                msg = message_form.save(commit=False)
                msg.sender   = request.user
                # ajustez suivant votre relation user/userprofile
                msg.receiver = house.proprietaire.user  
                msg.maison   = house
                msg.save()
                messages.success(request, "Message envoyé au propriétaire ✅")
            else:
                messages.error(request, "Le message est invalide.")
            return redirect('create_reservation', house_id=house.id)

        # 2️⃣ Gestion du clic « Make Reservation »
        if 'reserve' in request.POST and res_form.is_valid():
            reservation = res_form.save(commit=False)
            reservation.utilisateur = request.user.userprofile
            reservation.maison      = house
            reservation.statut      = 'en_attente'
            reservation.save()
            return redirect('process_payment', reservation_id=reservation.id)

    else:
        res_form     = ReservationForm()
        message_form = MessageForm()

    return render(request, 'reservation/create.html', {
        'house': house,
        'form': res_form,
        'message_form': message_form,
    })

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(utilisateur__user=request.user)
    return render(request, 'reservation/my_reservations.html', {'reservations': reservations})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur__user=request.user)
    if request.method == 'POST':
        reservation.statut = 'annulée'
        reservation.save()
        messages.success(request, 'Your reservation has been cancelled successfully.')
        return redirect('my_reservations')
    return render(request, 'reservation/cancel.html', {'reservation': reservation})


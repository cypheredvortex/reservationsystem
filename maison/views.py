from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Maison
from .forms import MaisonForm
from reservation.models import Reservation

def house_list(request):
    houses = Maison.objects.filter(disponible=True)
    return render(request, 'maison/house_list.html', {'houses': houses})

def house_detail(request, house_id):
    house = get_object_or_404(Maison, id=house_id)
    return render(request, 'maison/house_detail.html', {'house': house})

@login_required
def my_houses(request):
    houses = Maison.objects.filter(proprietaire__user=request.user)
    return render(request, 'maison/house_list.html', {'houses': houses, 'my_houses': True})

@login_required
def add_house(request):
    if request.method == 'POST':
        form = MaisonForm(request.POST, request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            house.proprietaire = request.user.userprofile
            house.save()
            messages.success(request, 'Property added successfully!')
            return redirect('my_houses')
    else:
        form = MaisonForm()
    return render(request, 'maison/add_house.html', {'form': form})

@login_required
def my_houses(request):
    houses = Maison.objects.filter(proprietaire=request.user.userprofile)
    return render(request, 'maison/my_houses.html', {'houses': houses})

@login_required
def edit_house(request, house_id):
    house = get_object_or_404(Maison, id=house_id, proprietaire=request.user.userprofile)
    if request.method == 'POST':
        form = MaisonForm(request.POST, instance=house)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('my_houses')
    return render(request, 'maison/edit_house.html', {'house': house})

@login_required
def delete_house(request, house_id):
    house = get_object_or_404(Maison, id=house_id, proprietaire__user=request.user)
    if request.method == 'POST':
        house.delete()
        messages.success(request, 'House deleted successfully!')
        return redirect('my_houses')
    return render(request, 'maison/house_confirm_delete.html', {'house': house})

@login_required
def received_reservations(request):
    if request.user.userprofile.role != 'proprietaire':
        messages.error(request, 'Only property owners can view received reservations.')
        return redirect('home')
    
    reservations = Reservation.objects.filter(maison__proprietaire__user=request.user)
    return render(request, 'maison/received_reservations.html', {'reservations': reservations})

def home(request):
    return render(request, 'home.html')

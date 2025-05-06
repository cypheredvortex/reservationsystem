from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from reservation.models import Reservation
from maison.models import Maison


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def profile_view(request):
    user_profile = request.user.userprofile
    role = user_profile.role

    context = {
        'user': request.user,
        'role': role,
    }

    if role == 'client':
        total_reservations = Reservation.objects.filter(utilisateur=user_profile).count()
        active_reservations = Reservation.objects.filter(utilisateur=user_profile, statut='confirmée').count()
        context.update({
            'total_reservations': total_reservations,
            'active_reservations': active_reservations,
        })

    elif role == 'proprietaire':
        total_properties = Maison.objects.filter(proprietaire=user_profile).count()
        active_properties = Maison.objects.filter(proprietaire=user_profile, disponible=True).count()
        context.update({
            'total_properties': total_properties,
            'active_properties': active_properties,
        })

    return render(request, 'user/profile.html', context)

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé')
        return redirect('home')
        
    users = User.objects.all()
    return render(request, 'user/manage_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé')
        return redirect('home')
        
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Utilisateur supprimé avec succès!')
        return redirect('manage_users')
    return render(request, 'user/user_confirm_delete.html', {'user': user})

@login_required
def all_reservations(request):
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé')
        return redirect('home')
        
    reservations = Reservation.objects.all()
    return render(request, 'user/all_reservations.html', {'reservations': reservations})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'user/profile.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import render

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'user/logout.html')  # Assure-toi que ce fichier existe

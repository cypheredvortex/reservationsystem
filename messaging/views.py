# messaging/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import MessageForm
from .models import Message
from maison.models import Maison


@login_required
def send_message(request, maison_id):
    """
    Envoie un message du client vers le propriétaire.
    """
    maison = get_object_or_404(Maison, pk=maison_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = maison.proprietaire.user
            msg.maison = maison
            msg.save()
            messages.success(request, "Votre message a été envoyé ✅")
        else:
            messages.error(request, "Erreur dans votre message.")
    return redirect('maison_detail', house_id=maison_id)


@login_required
def inbox(request):
    """
    Boîte de réception pour le propriétaire.
    """
    profile = getattr(request.user, 'userprofile', None)
    if not profile or profile.role != 'proprietaire':
        messages.error(request, "Accès réservé aux propriétaires.")
        return redirect('house_list')

    received = Message.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'messaging/inbox.html', {
        'messages': received,
    })


@login_required
def sent_messages(request):
    """
    Liste des messages envoyés par l'utilisateur.
    """
    sent = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'messaging/sent.html', {
        'sent_messages': sent,
    })


@login_required
def conversation(request, message_id):
    """
    Affiche une conversation (message initial + fil).
    Permet à l'expéditeur OU au destinataire de poster une réponse.
    """
    original = get_object_or_404(Message, id=message_id)

    # 1️⃣ Sécurité : seul client ou propriétaire peuvent y accéder
    if request.user not in (original.sender, original.receiver):
        messages.error(request, "Conversation inaccessible.")
        return redirect('house_list')

    # 2️⃣ Préparer le formulaire de réponse pour l'un OU l'autre
    reply_form = None
    if request.user in (original.sender, original.receiver):
        if request.method == 'POST':
            reply_form = MessageForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.sender = request.user
                # Si c'est le client qui répond, envoyer au propriétaire, et inversement
                if request.user == original.sender:
                    reply.receiver = original.receiver
                else:
                    reply.receiver = original.sender
                reply.maison = original.maison
                reply.parent = original
                reply.save()
                messages.success(request, "Votre réponse a été envoyée ✅")
                return redirect('conversation', message_id=message_id)
            else:
                messages.error(request, "Le message ne peut pas être vide.")
        else:
            reply_form = MessageForm()

    # 3️⃣ Récupérer le fil de discussion
    thread = original.replies.all().order_by('created_at')

    return render(request, 'messaging/conversation.html', {
        'original': original,
        'thread': thread,
        'reply_form': reply_form,
    })
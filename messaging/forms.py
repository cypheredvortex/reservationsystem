# messaging/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2, 'placeholder': 'Votre message…'}),
        label=''
    )
    class Meta:
        model = Message
        fields = ['content']
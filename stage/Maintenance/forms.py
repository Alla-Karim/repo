from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PhotosMachines, Machine

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = [
            'ref_constructeur',
            'poste',
            'etat',
            'date_achat',
            'date_derniere_maintenance',
        ]
        widgets = {
            'date_achat': forms.DateInput(attrs={'type': 'date'}),
            'date_derniere_maintenance': forms.DateInput(attrs={'type': 'date'}),
        }


class SaisisseurForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requis. Exemple : user@example.com")
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user

class PhotoMachineForm(forms.ModelForm):
    google_drive_url = forms.URLField(
        label="Lien Google Drive",
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://drive.google.com/…'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description (optionnelle)'})
    )

    class Meta:
        model = PhotosMachines
        fields = ['google_drive_url', 'description']  # Plus de champ 'machine'

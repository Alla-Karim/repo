from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import get_object_or_404

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts  import redirect


from .models import *
from .forms import MachineForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

from openpyxl import Workbook
from io import BytesIO

import openpyxl
from django.http import HttpResponse
from .models import Machine



def is_saisisseur(user):
    return user.is_authenticated and not user.is_superuser

def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
def machine_list(request):
    machines = Machine.objects.all()
    return render(request, 'machine_list.html', {'machines': machines})

@login_required
def machine_create(request):
    form = MachineForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('machine_list')
    return render(request, 'machine_form.html', {'form': form, 'title': 'Ajouter une machine'})

@login_required
def machine_update(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    form = MachineForm(request.POST or None, instance=machine)
    if form.is_valid():
        form.save()
        return redirect('machine_list')
    return render(request, 'machine_form.html', {'form': form, 'title': 'Modifier une machine'})

@login_required
def machine_delete(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    if request.method == 'POST':
        machine.delete()
        return redirect('machine_list')
    return render(request, 'machine_confirm_delete.html', {'machine': machine})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # crée l'utilisateur
            messages.success(request, f"Compte créé pour {user.username} !")
            return redirect('login')
        else:
            messages.error(request, "Erreur dans le formulaire")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    operateurs = Operateur.objects.all().order_by('nom')
    machines = Machine.objects.all().order_by('ref_constructeur')
    saisisseurs = User.objects.filter(is_superuser=False).order_by('username')
    
    context = {
        'operateurs': operateurs,
        'machines': machines,
        'saisisseurs': saisisseurs,
    }
    return render(request, 'admin_panel/dashboard.html', context)  # <== chemin corrigé

def export_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Machines"

    # En-têtes
    ws.append(["Référence", "Poste", "État", "Date d'achat", "Date dernière maintenance"])

    # Données
    for machine in Machine.objects.all():
        ws.append([
            machine.ref_constructeur,
            machine.poste.nom if machine.poste else "N/A",
            machine.etat,
            machine.date_achat.strftime('%Y-%m-%d') if machine.date_achat else '',
            machine.date_derniere_maintenance.strftime('%Y-%m-%d') if machine.date_derniere_maintenance else ''
        ])

    # Utiliser BytesIO au lieu de save_virtual_workbook
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=machines.xlsx'
    return response


def home(request):
    return render(request, 'home.html')



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/admin-panel/'  # ton dashboard admin personnalisé
        else:
            return super().get_success_url()

def saisisseur_add(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Saisisseur {user.username} ajouté avec succès !")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Merci de corriger les erreurs ci-dessous.")
    else:
        form = UserCreationForm()
    return render(request, 'admin_panel/saisisseur_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def saisisseur_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, f"Saisisseur {user.username} supprimé avec succès.")
        return redirect('admin_dashboard')
    return render(request, 'admin_panel/saisisseur_confirm_delete.html', {'user': user})
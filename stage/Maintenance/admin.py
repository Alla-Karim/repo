from django.contrib import admin
from .models import Machine, Operateur, Poste, LigneProduction

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('ref_constructeur', 'poste', 'etat', 'date_achat', 'date_derniere_maintenance')
    list_filter = ('etat', 'poste')
    search_fields = ('ref_constructeur',)
    ordering = ('ref_constructeur',)

@admin.register(Operateur)
class OperateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email')
    search_fields = ('nom', 'prenom', 'email')

@admin.register(Poste)
class PosteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ligne', 'operateur')
    list_filter = ('ligne',)
    search_fields = ('nom',)

@admin.register(LigneProduction)
class LigneProductionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)

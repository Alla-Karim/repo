from django.db import models

class Operateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class LigneProduction(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class Poste(models.Model):
    nom = models.CharField(max_length=100)
    ligne = models.ForeignKey(LigneProduction, on_delete=models.CASCADE, related_name='postes')
    operateur = models.OneToOneField(Operateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='poste')

    def __str__(self):
        return f"{self.nom} (Ligne : {self.ligne.nom})"

class Machine(models.Model):
    ref_constructeur = models.CharField(max_length=50, unique=True)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE, related_name='machines', null=True, blank=True)
    etat = models.CharField(
        max_length=20,
        choices=[
            ('fonctionnel', 'Fonctionnel'),
            ('en_panne', 'En panne'),
            ('maintenance', 'Maintenance'),
            ('hors_service', 'Hors service')
        ],
        default='fonctionnel'
    )
    date_achat = models.DateField()
    date_derniere_maintenance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Machine {self.ref_constructeur} ({self.etat})"

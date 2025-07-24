import mysql.connector
import random
from datetime import date, timedelta

# Connexion MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='alla',
    password='12345',  # remplace par ton vrai mot de passe
    database='BD'
)
cursor = conn.cursor()

etats = ['fonctionnel', 'en_panne', 'maintenance', 'hors_service']
machines = []

for i in range(1, 21):
    ref = f"26210{i:03d}"
    etat = random.choice(etats)
    poste_id = random.randint(1, 12)

    # Génération de dates
    date_achat = date(2021, random.randint(1, 12), random.randint(1, 28))
    date_maintenance = date_achat + timedelta(days=random.randint(30, 900))

    machines.append((
        ref,
        poste_id,
        etat,
        date_achat.isoformat(),
        date_maintenance.isoformat()
    ))

# Insertion dans la table Machine
cursor.executemany("""
    INSERT INTO Maintenance_machine (
        ref_constructeur, poste_id, etat, date_achat, date_derniere_maintenance
    ) VALUES (%s, %s, %s, %s, %s)
""", machines)

conn.commit()
print("✅ 20 machines insérées avec succès.")

cursor.close()
conn.close()

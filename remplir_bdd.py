import sqlite3

# Connexion (ou création) de la base de données
conn = sqlite3.connect('citizens.db')
cursor = conn.cursor()

# Création de la table mitarbeiter s'il n'existe pas déjà
cursor.execute('''
CREATE TABLE IF NOT EXISTS mitarbeiter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    UID TEXT,
    vorname TEXT,
    nachname TEXT,
    adresse TEXT,
    telefonnummer TEXT,
    bild TEXT
)
''')

# Données des mitarbeiter
mitarbeiter_daten = [
    ("04A5A10AAF0590", "Hanane", "Aidouni", "Köngen", "01792983523", "hanane.jpg"),
    ("04A5A10AAF0591", "Marc", "Wilms", "Stuttgart", "01782983522", "marc.jpg"),
    ("04A5A11AAF0590", "Laura", "Müller", "Wendlingen", "01782983511", "laura.jpg")
]

cursor.executemany('''
    INSERT INTO mitarbeiter (UID, vorname, nachname, adresse, telefonnummer, bild)
    VALUES (?, ?, ?, ?, ?, ?)
''', mitarbeiter_daten)

conn.commit()
conn.close()

print("✅ Die Datenbank wurde erfolgreich mit Mitarbeiter-Daten befüllt.")

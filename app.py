from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'citizens.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Création de la table si elle n'existe pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mitarbeiter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        UID TEXT UNIQUE,
        vorname TEXT,
        nachname TEXT,
        adresse TEXT,
        telefonnummer TEXT,
        bild TEXT
    )
    ''')
    # Vérifie si la table est vide
    cursor.execute("SELECT COUNT(*) FROM mitarbeiter")
    count = cursor.fetchone()[0]
    if count == 0:
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

def get_mitarbeiter_data(barcode):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT vorname, nachname, adresse, telefonnummer, bild FROM mitarbeiter WHERE UID = ?", (barcode,))
    data = cursor.fetchone()
    conn.close()
    return data

@app.route('/', methods=['GET', 'POST'])
def home():
    mitarbeiter = None
    error = None
    if request.method == 'POST':
        barcode = request.form.get('barcode', '').strip()
        if barcode:
            mitarbeiter = get_mitarbeiter_data(barcode)
            if not mitarbeiter:
                error = "❌ Mitarbeiter nicht gefunden."
        else:
            error = "Le champ UID est vide."
    return render_template('home.html', mitarbeiter=mitarbeiter, error=error)

if __name__ == '__main__':
    init_db()  # <-- IMPORTANT : création / insertion dans la base avant de lancer le serveur
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

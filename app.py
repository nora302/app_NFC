from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'citizens.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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

def get_mitarbeiter_data(uid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT vorname, nachname, adresse, telefonnummer, bild FROM mitarbeiter WHERE UID = ?", (uid,))
    data = cursor.fetchone()
    conn.close()
    return data

@app.route('/', methods=['GET', 'POST'])
def home():
    mitarbeiter = None
    error = None
    success = None

    # --- NFC tag UID handling from URL ---
    uid_param = request.args.get('uid')
    if uid_param:
        mitarbeiter = get_mitarbeiter_data(uid_param)
        if not mitarbeiter:
            error = "❌ Mitarbeiter mit diesem UID wurde nicht gefunden."
        return render_template('home.html', mitarbeiter=mitarbeiter, error=error, success=success)

    # --- Form handling ---
    if request.method == 'POST':
        action = request.form.get('action')
        barcode = request.form.get('barcode', '').strip()
        
        if action == 'search':
            if barcode:
                mitarbeiter = get_mitarbeiter_data(barcode)
                if not mitarbeiter:
                    error = "❌ Mitarbeiter nicht gefunden."
            else:
                error = "UID Feld ist leer."
        
        elif action == 'add':
            if barcode:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO mitarbeiter (UID, vorname, nachname, adresse, telefonnummer, bild)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (barcode, 'Neu', 'Mitarbeiter', 'Adresse', '0000000000', 'default.jpg'))
                    conn.commit()
                    conn.close()
                    success = "✅ Neuer Mitarbeiter erfolgreich hinzugefügt."
                except sqlite3.IntegrityError:
                    error = "❌ Mitarbeiter mit dieser UID existiert bereits."
            else:
                error = "UID Feld ist leer."

    return render_template('home.html', mitarbeiter=mitarbeiter, error=error, success=success)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

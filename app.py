from flask import Flask, render_template, request, url_for
import sqlite3
import os

app = Flask(__name__)

def get_mitarbeiter_data(barcode):
    conn = sqlite3.connect('citizens.db')
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
        try:
            barcode = request.form.get('barcode', '').strip()
            if barcode:
                mitarbeiter = get_mitarbeiter_data(barcode)
                if mitarbeiter:
                    image_path = os.path.join(app.static_folder, 'photos', mitarbeiter[4])
                    if not os.path.isfile(image_path):
                        error = f"L’image {mitarbeiter[4]} est introuvable."
                        mitarbeiter = None
                else:
                    error = "❌ Mitarbeiter nicht gefunden."
            else:
                error = "Le champ UID est vide."
        except Exception as e:
            error = f"Erreur serveur : {str(e)}"

    return render_template('home.html', mitarbeiter=mitarbeiter, error=error)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

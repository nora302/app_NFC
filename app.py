from flask import Flask, render_template, request
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
    if request.method == 'POST':
        barcode = request.form.get('barcode', '')
        mitarbeiter = get_mitarbeiter_data(barcode)
    return render_template('home.html', mitarbeiter=mitarbeiter)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 50000))
    app.run(host='0.0.0.0', port=port, debug=True)

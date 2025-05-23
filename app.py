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
    if request.method == 'POST':
        barcode = request.form['barcode']
        mitarbeiter = get_mitarbeiter_data(barcode)
        if mitarbeiter:
            return render_template('result.html', mitarbeiter=mitarbeiter)
        else:
            return "Mitarbeiter nicht gefunden."
    return render_template('home.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

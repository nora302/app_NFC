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

def get_mitarbeiter_data(barcode):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT vorname, nachname, adresse, telefonnummer, bild F

from flask import Flask, render_template, request, redirect, url_for
import os
import firebase_admin
from firebase_admin import credentials, firestore

APP_VERSION = "1.0.0"

app = Flask(__name__)

# Initialize Firebase Admin SDK
# Ensure 'firebase-service-account.json' is in the same directory as app.py
# or provide the correct path to your service account key file.
# For production, consider using environment variables for the path or credentials.
try:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    print("Please ensure 'firebase-service-account.json' is correctly configured.")
    db = None # Set db to None if initialization fails


@app.route('/', methods=['GET', 'POST'])
def index():
    if db is None:
        return "Firestore initialization failed. Check your service account key.", 500

    if request.method == 'POST':
        note_content = request.form.get('note')
        if note_content:
            db.collection('notes').add({'content': note_content, 'timestamp': firestore.SERVER_TIMESTAMP})
        return redirect(url_for('index'))
    
    notes = []
    try:
        notes_ref = db.collection('notes').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
        for doc in notes_ref:
            note = doc.to_dict()
            note['id'] = doc.id
            notes.append(note)
    except Exception as e:
        print(f"Error fetching notes from Firestore: {e}")
        # Optionally, you can render an error message to the user
        return "Error fetching notes.", 500

    return render_template('index.html', notes=notes, app_version=APP_VERSION)

@app.route('/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    if db is None:
        return "Firestore initialization failed. Check your service account key.", 500
    try:
        db.collection('notes').document(note_id).delete()
    except Exception as e:
        print(f"Error deleting note from Firestore: {e}")
        # Optionally, you can render an error message to the user
        return "Error deleting note.", 500
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
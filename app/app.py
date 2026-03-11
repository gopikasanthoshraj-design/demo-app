import os
from flask import Flask, render_template, request, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

# --- App Configuration ---
APP_VERSION = "1.0.0"  # You can change this version for updates
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"

# --- Firebase Configuration ---
# Use the GOOGLE_APPLICATION_CREDENTIALS environment variable to locate the credentials
firebase_cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'serviceAccountKey.json')

try:
    if firebase_cred_path:
        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully.")
    else:
        db = None
        print("Firebase not initialized. Check your credentials setup.")
        flash("Firebase not initialized. Please check your credentials setup.")
except Exception as e:
    db = None
    flash(f"Error initializing Firebase: {e}")
    print(f"Error initializing Firebase: {e}")

# --- Flask App Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')  # Use a strong secret key in production

# --- Routes ---
@app.route('/')
def index():
    notes = []
    if db:
        try:
            # Fetch notes from Firestore
            notes_ref = db.collection('notes').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
            for doc in notes_ref:
                note = doc.to_dict()
                note['id'] = doc.id
                notes.append(note)
        except Exception as e:
            flash(f"Error fetching notes from Firestore: {e}")
            print(f"Error fetching notes from Firestore: {e}")
    return render_template('index.html', notes=notes, app_version=APP_VERSION)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash("Both title and content are required!")
            return redirect(url_for('add_note'))
        
        if db:
            try:
                db.collection('notes').add({
                    'title': title,
                    'content': content,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
                flash("Note added successfully!")
                return redirect(url_for('index'))
            except Exception as e:
                flash(f"Error adding note to Firestore: {e}")
                print(f"Error adding note to Firestore: {e}")
        else:
            flash("Firebase database is not available. Please check your credentials setup.")
    
    return render_template('add_note.html', app_version=APP_VERSION)

# --- Main Entry Point ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Cloud Run expects the port to be set via this env variable
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=port)
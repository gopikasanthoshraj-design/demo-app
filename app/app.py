import os
from flask import Flask, render_template, request, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

# --- App Configuration ---
APP_VERSION = "1.0.0"
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"

# --- Firebase Configuration ---
# Initialize Firebase
try:
    # Attempt to initialize Firebase from environment variable
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        cred = credentials.ApplicationDefault()
    else:
        # Fallback to local file if not in environment
        cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
        else:
            flash("WARNING: 'serviceAccountKey.json' not found and GOOGLE_APPLICATION_CREDENTIALS not set. Firestore functionality will be limited or fail.")
            print("WARNING: 'serviceAccountKey.json' not found and GOOGLE_APPLICATION_CREDENTIALS not set.")
            cred = None

    if cred:
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully.")
    else:
        db = None
        print("Firebase not initialized. Check your credentials setup.")
        flash("Firebase not initialized. Check your credentials setup.")

except Exception as e:
    db = None
    flash(f"Error initializing Firebase: {e}. Firestore functionality will be unavailable.")
    print(f"Error initializing Firebase: {e}")
    print("Firestore functionality will be unavailable.")

# --- Flask App Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')  # Consider using a secret key from env variables

# --- Routes ---

@app.route('/')
def index():
    notes = []
    if db:
        try:
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
            flash("Title and content are required fields!")
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
            flash("Firebase database is not available. Please check your configuration.")
    
    return render_template('add_note.html', app_version=APP_VERSION)

# --- Main Entry Point ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=port)
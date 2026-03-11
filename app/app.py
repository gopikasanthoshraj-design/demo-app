import os
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

# --- App Configuration ---
APP_VERSION = "1.0.0"
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"

# --- Firebase Configuration ---
# You need to provide your Firebase service account key.
# For local development, you can place a 'serviceAccountKey.json' file
# in the same directory as app.py or set the GOOGLE_APPLICATION_CREDENTIALS
# environment variable.
# For deployment, consider using environment variables or other secure methods.

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
            print("WARNING: 'serviceAccountKey.json' not found and GOOGLE_APPLICATION_CREDENTIALS not set.")
            print("Firestore functionality will be limited or fail.")
            cred = None

    if cred:
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully.")
    else:
        db = None
        print("Firebase not initialized. Check your credentials setup.")

except Exception as e:
    db = None
    print(f"Error initializing Firebase: {e}")
    print("Firestore functionality will be unavailable.")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # Replace with a strong secret key in production

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
            print(f"Error fetching notes from Firestore: {e}")
            # Optionally, add a flash message for the user
    return render_template('index.html', notes=notes, app_version=APP_VERSION)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content and db:
            try:
                db.collection('notes').add({
                    'title': title,
                    'content': content,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
                return redirect(url_for('index'))
            except Exception as e:
                print(f"Error adding note to Firestore: {e}")
                # Optionally, add a flash message for the user
        else:
            # Handle cases where title or content is missing, or db is not initialized
            pass # For now, just render the form again
    return render_template('add_note.html', app_version=APP_VERSION)

# You can add more routes for editing, deleting, etc.

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

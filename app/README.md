# Note-Taking Flask App with Firestore

This project is a simple Flask-based frontend for a note-taking application that uses Google Cloud Firestore as its backend database. It includes a version number and a Dockerfile for easy containerization.

## Project Structure

```
new-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── templates/
    ├── index.html
    └── add_note.html
```

## Setup and Running

### 1. Google Cloud Firestore Credentials

To connect to Firestore, you need a service account key.

**Option A: Using `GOOGLE_APPLICATION_CREDENTIALS` environment variable (Recommended for production)**

1.  Go to the Google Cloud Console.
2.  Navigate to "IAM & Admin" > "Service Accounts".
3.  Create a new service account or select an existing one.
4.  Create a new JSON key for the service account and download it.
5.  Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of this JSON file.
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"
    ```

**Option B: Placing `serviceAccountKey.json` locally (For local development only)**

Place the downloaded `serviceAccountKey.json` file directly in the `new-app/` directory alongside `app.py`. **Do not commit this file to version control.** For this reason, `.dockerignore` explicitly excludes this file.

### 2. Local Development (without Docker)

1.  **Navigate to the project directory:**
    ```bash
    cd new-app
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Flask application:**
    ```bash
    export FLASK_APP=app.py
    flask run --host=0.0.0.0 --port=5000
    ```
    (Ensure your Firebase credentials are set up as described above.)
5.  Open your browser to `http://127.0.0.1:5000`.

### 3. Docker Deployment

1.  **Navigate to the project directory:**
    ```bash
    cd new-app
    ```
2.  **Build the Docker image:**
    ```bash
    docker build -t note-app:1.0.0 .
    ```
3.  **Run the Docker container:**

    *   **If using `GOOGLE_APPLICATION_CREDENTIALS` environment variable:**
        ```bash
        docker run -p 5000:5000 -e GOOGLE_APPLICATION_CREDENTIALS="/path/in/container/serviceAccountKey.json" -v /path/to/your/serviceAccountKey.json:/path/in/container/serviceAccountKey.json note-app:1.0.0
        ```
        Replace `/path/to/your/serviceAccountKey.json` with the host path to your service account key.

    *   **If you placed `serviceAccountKey.json` directly in the `new-app/` directory (for testing):**
        ```bash
        docker run -p 5000:5000 note-app:1.0.0
        ```
        In this case, the `serviceAccountKey.json` will be copied into the image if it's present during build and not excluded by `.dockerignore`. However, the `.dockerignore` I provided *excludes* `serviceAccountKey.json` to encourage better security practices. Therefore, the first Docker run command with volume mounting is the preferred method for passing credentials securely into the container.

4.  Open your browser to `http://localhost:5000`.

## Application Version

The application version is `1.0.0` and is displayed on the bottom of the `index.html` and `add_note.html` pages.

## Features

*   **View Notes:** Displays a list of notes with their title, content, and creation timestamp.
*   **Add Notes:** Provides a form to add new notes to the Firestore database.
*   **Firestore Backend:** Uses Google Cloud Firestore for persistent storage of notes.
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Path to your service account key
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()
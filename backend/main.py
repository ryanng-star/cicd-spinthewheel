import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore

# 1. Initialize the Flask App and the CORS Bouncer
app = Flask(__name__)
CORS(app) # Allows your frontend to talk to this backend safely

# 2. Initialize the Firestore Database Client
db = firestore.Client()
COLLECTION_NAME = "restaurants"

# -------------------------------------------------------------------------
# ROUTE 1: The Health Check (Required by Cloud Run)
# -------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def health_check():
    """Cloud Run pings this URL to make sure the server is awake."""
    return jsonify({"status": "healthy", "message": "The Kitchen is open!"}), 200

# -------------------------------------------------------------------------
# ROUTE 2: Get all Restaurants (For the Wheel)
# -------------------------------------------------------------------------
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    """Fetches the list of restaurants from Firestore."""
    try:
        # Pull all documents from the "restaurants" collection
        docs = db.collection(COLLECTION_NAME).stream()
        
        restaurant_list = []
        for doc in docs:
            data = doc.to_dict()
            restaurant_list.append({
                "id": doc.id,
                "name": data.get("name")
            })
            
        return jsonify({"restaurants": restaurant_list}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------------------------------------------------
# ROUTE 3: Add a new Restaurant
# -------------------------------------------------------------------------
@app.route('/restaurants', methods=['POST'])
def add_restaurant():
    """Saves a new restaurant to Firestore."""
    try:
        # Read the JSON data sent by the frontend
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({"error": "Please provide a 'name' field"}), 400
            
        restaurant_name = data['name']
        
        # Create a new document in Firestore
        doc_ref = db.collection(COLLECTION_NAME).document()
        doc_ref.set({
            "name": restaurant_name,
            "added_at": firestore.SERVER_TIMESTAMP
        })
        
        return jsonify({"message": f"Added '{restaurant_name}' successfully!", "id": doc_ref.id}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------------------------------------------------
# SERVER STARTUP
# -------------------------------------------------------------------------
if __name__ == '__main__':
    # Cloud Run requires the app to listen on a specific port (default 8080)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
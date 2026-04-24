import os
import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------------------------------------------------------------------------
# ROUTE 1: Encode (List -> Gibberish)
# -------------------------------------------------------------------------
@app.route('/api/encode', methods=['POST'])
def encode_wheel():
    """Takes a list of restaurants and turns it into a URL-safe string."""
    try:
        # 1. Get the list of restaurants from the frontend
        data = request.get_json()
        restaurant_list = data.get("restaurants", [])
        
        # 2. Convert the list into a JSON string
        json_string = json.dumps(restaurant_list)
        
        # 3. Compress/Encode it into Base64 gibberish
        encoded_bytes = base64.urlsafe_b64encode(json_string.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        
        # 4. Send the gibberish back
        return jsonify({"token": encoded_string}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------------------------------------------------
# ROUTE 2: Decode (Gibberish -> List)
# -------------------------------------------------------------------------
@app.route('/api/decode', methods=['POST'])
def decode_wheel():
    """Takes a URL-safe string and turns it back into a list of restaurants."""
    try:
        # 1. Get the gibberish token from the frontend
        data = request.get_json()
        token = data.get("token", "")
        
        # 2. Decode the Base64 back into a JSON string
        decoded_bytes = base64.urlsafe_b64decode(token.encode('utf-8'))
        json_string = decoded_bytes.decode('utf-8')
        
        # 3. Convert the JSON string back into a Python list
        restaurant_list = json.loads(json_string)
        
        # 4. Send the list back to the frontend
        return jsonify({"restaurants": restaurant_list}), 200
        
    except Exception as e:
        return jsonify({"error": "Invalid or corrupted link."}), 400

# -------------------------------------------------------------------------
# SERVER STARTUP
# -------------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
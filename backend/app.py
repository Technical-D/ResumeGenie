from flask import Flask, request, jsonify
import os
from api_key_manager import connect_db
from parser import parse_resume
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/parse_resume": {"origins": "*"}})

def check_api_key(api_key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_keys WHERE api_key=?", (api_key,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    return False


@app.route('/parse_resume', methods=['POST'])
@cross_origin(origins="*")
def main():
    api_key = request.headers.get('API-Key')
    print(api_key)
    if not api_key or not check_api_key(api_key):
        return jsonify({"error": "Invalid or missing API Key"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Unsupported file format. Please upload a PDF file."}), 400

    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    parsed_data = parse_resume(file_path)

    return jsonify(parsed_data), 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,API-Key')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    return response

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(debug=True)



from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
 
# Add the eda_analysis directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'eda_analysis'))
 
from eda import process_files
 
app = Flask(__name__)
CORS(app)
 
@app.route('/api/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files uploaded"}), 400
 
    data_info = process_files(files)
    if "error" in data_info:
        return jsonify(data_info), 400
 
    return jsonify(data_info)
 
if __name__ == '__main__':
    app.run(debug=True)
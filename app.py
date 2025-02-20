from flask import Flask, request, render_template, jsonify # type: ignore
from flask_socketio import SocketIO # type: ignore
from models import db, Dataset
from config import Config
from ml_model import compute_similarity, detect_anomaly
from hashlib import sha256
import os
from datetime import datetime
import time
from flask import Flask, redirect, url_for

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
socketio = SocketIO(app)

# Function to read file content
def read_file_content(file_path):
    with open(file_path, 'rb') as file:  # Open as binary to handle all file types
        return file.read()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Read file content and calculate checksum
    try:
        file_content = read_file_content(file_path)
    except Exception as e:
        os.remove(file_path)
        return jsonify({'error': f'Could not read file content: {str(e)}'}), 400

    checksum = sha256(file_content).hexdigest()
    size = os.path.getsize(file_path)

    # Check if the checksum already exists in the database
    existing_dataset = Dataset.query.filter_by(checksum=checksum).first()
    if existing_dataset:
        os.remove(file_path)  # Remove the duplicate file
        return render_template('alert.html', dataset=existing_dataset) # Show alert for duplicate
    

    # Detect anomalies based on the file's size and timestamp (e.g., time of day)
    is_anomalous = detect_anomaly([size, datetime.now().hour])
    if is_anomalous:
        os.remove(file_path)  # Remove anomalous file
        return render_template('error.html')

    # Save metadata to the database
    new_dataset = Dataset(
        name=file.filename,
        checksum=checksum,
        size=size,
        location=file_path,
        timestamp=datetime.now()
    )
    db.session.add(new_dataset)
    db.session.commit()

    socketio.emit('upload_success', {
        'name': file.filename,
        'size': size,
        'timestamp': new_dataset.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })

    return render_template('right.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database if not created
    socketio.run(app, host='127.0.0.1', port=8000, debug=True)

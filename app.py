import os
import numpy as np
import cv2
import tensorflow as tf
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import uuid
import warnings

# Add this right after importing TensorFlow
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.set_visible_devices([], 'GPU')

warnings.filterwarnings('ignore')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['HISTORY_FILE'] = 'image_history.json'
app.config['SECRET_KEY'] = 'your-secret-key-here'  # For sessions and flash messages
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the model
model = tf.keras.models.load_model('./ml_model/traffic_sign.h5', compile=False)

# Recompile the model with a compatible optimizer
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Define class names
class_names = np.array(['Speed limit (20km/h)', 'Speed limit (30km/h)', 'Speed limit (50km/h)', 
                        'Speed limit (60km/h)', 'Speed limit (70km/h)', 'Speed limit (80km/h)', 
                        'End of speed limit (80km/h)', 'Speed limit (100km/h)', 'Speed limit (120km/h)', 
                        'No passing', 'No passing for vehicles over 3.5 metric tons', 
                        'Right-of-way at the next intersection', 'Priority road', 'Yield', 'Stop', 
                        'No vehicles', 'Vehicles over 3.5 metric tons prohibited', 'No entry', 
                        'General caution', 'Dangerous curve to the left', 'Dangerous curve to the right', 
                        'Double curve', 'Bumpy road', 'Slippery road', 'Road narrows on the right', 
                        'Road work', 'Traffic signals', 'Pedestrians', 'Children crossing', 
                        'Bicycles crossing', 'Beware of ice/snow', 'Wild animals crossing', 
                        'End of all speed and passing limits', 'Turn right ahead', 'Turn left ahead', 
                        'Ahead only', 'Go straight or right', 'Go straight or left', 'Keep right', 
                        'Keep left', 'Roundabout mandatory', 'End of no passing', 
                        'End of no passing by vehicles over 3.5 metric tons'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (32, 32))
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype('float32') / 255.0
    return img_array

def save_to_history(image_path, filename, class_label, confidence, user_id=None):
    """Save prediction to history file"""
    history_path = app.config['HISTORY_FILE']
    
    # Generate a unique ID for this prediction
    prediction_id = str(uuid.uuid4())
    
    # Create history entry
    entry = {
        'id': prediction_id,
        'filename': filename,
        'class_label': class_label,
        'confidence': float(confidence),  # Convert numpy float32 to Python float
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': user_id
    }
    
    # Load existing history
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []
    
    # Add new entry and save
    history.append(entry)
    
    # Keep only the last 50 entries (optional)
    if len(history) > 50:
        history = history[-50:]
    
    with open(history_path, 'w') as f:
        json.dump(history, f)
    
    return prediction_id

def get_history(user_id=None):
    """Retrieve prediction history, optionally filtered by user"""
    history_path = app.config['HISTORY_FILE']
    
    if not os.path.exists(history_path):
        return []
    
    with open(history_path, 'r') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []
    
    # Sort by timestamp (most recent first)
    history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # If user_id provided, filter by user
    if user_id:
        history = [entry for entry in history if entry.get('user_id') == user_id]
    
    return history

def predict_traffic_sign(image_path):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    
    # Get top 3 predictions
    top_indices = np.argsort(predictions[0])[-3:][::-1]
    
    # Main prediction (highest confidence)
    class_idx = top_indices[0]
    class_confidence = predictions[0][class_idx] * 100
    
    # Alternative predictions - as a list, not numpy array
    top_predictions = []
    for i in range(1, len(top_indices)):
        idx = top_indices[i]
        conf = predictions[0][idx] * 100
        if conf > 5:  # Only include if confidence is above 5%
            top_predictions.append({
                'label': class_names[idx],
                'confidence': f"{conf:.2f}%"
            })
    
    if class_confidence > 90:
        return class_names[class_idx], class_confidence, top_predictions
    else:
        return "Not Sure", class_confidence, top_predictions

@app.route('/')
def index():
    # Get recent predictions for the gallery
    recent_predictions = get_history()[:8]  # Show up to 8 recent predictions
    return render_template('index.html', recent_predictions=recent_predictions)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        class_label, confidence, top_predictions = predict_traffic_sign(file_path)
        
        # Save to history (get user_id from session if available)
        user_id = session.get('user_id') if 'user_id' in session else None
        prediction_id = save_to_history(file_path, filename, class_label, confidence, user_id)
        
        return render_template('result.html', 
                              filename=filename,
                              class_label=class_label,
                              confidence=f"{confidence:.2f}%",
                              confidence_value=confidence,
                              prediction_id=prediction_id,
                              top_predictions=top_predictions)
    
    return jsonify({'error': 'File type not allowed'})

@app.route('/gallery')
def gallery():
    """Show gallery of all predictions"""
    # Get user_id from session if logged in
    user_id = session.get('user_id') if 'user_id' in session else None
    
    # If user is logged in and viewing their own gallery, show only their predictions
    show_personal = request.args.get('personal', 'false').lower() == 'true' and user_id
    
    if show_personal:
        history = get_history(user_id)
        title = "My Prediction History"
    else:
        history = get_history()
        title = "Recent Predictions Gallery"
    
    return render_template('gallery.html', history=history, title=title)

@app.route('/prediction/<prediction_id>')
def view_prediction(prediction_id):
    """View a specific prediction"""
    history = get_history()
    prediction = next((p for p in history if p.get('id') == prediction_id), None)
    
    if not prediction:
        flash("Prediction not found")
        return redirect(url_for('gallery'))
    
    return render_template('prediction.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 
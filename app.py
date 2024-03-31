from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os

# Flask configuration and initial setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to render the home page
@app.route('/')
def home():
    # No image to display initially
    return render_template('home.html', image_url=None)

# Route to handle diagnosis and image upload
@app.route('/diagnosis', methods=['POST'])
def diagnose():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Save the secure filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        counter = 1
        # If file exists, append a counter to its name
        while os.path.exists(filepath):
            name, extension = os.path.splitext(filename)
            filename = f"{name}_{counter}{extension}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        file.save(filepath)
        
        # Placeholder for actual prediction logic
        predicted_bowel_health = '80%'  # Replace with actual logic
        
        # Generate the URL for the uploaded image
        image_url = url_for('uploaded_file', filename=filename)
        
        # Render the diagnosis page with the image and prediction
        return render_template('diagnose.html', bowel_health=predicted_bowel_health, image_url=image_url)

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

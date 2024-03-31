from flask import Flask, render_template, request, url_for, session
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
import gradio as gr
import os
import threading
from openai import OpenAI
from PIL import Image
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
# Flask configuration and initial setup
app = Flask(__name__)
app.secret_key = 'vetview'
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

client = OpenAI(
    # Replace with your valid API key
    api_key="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"
)


@app.route('/')
def home():
    # No image to display initially
    return render_template('home.html', image_url=None)

@app.route('/diagnosis', methods=['POST'])
def diagnose():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    session['breed_type'] = request.form['breed_type']
    session['age_dog'] = request.form['age']
    if file.filename == '':
        return 'No selected file'

    #run file through model
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        counter = 1
        while os.path.exists(filepath):
            name, extension = os.path.splitext(filename)
            filename = f"{name}_{counter}{extension}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        file.save(filepath)
        image = Image.open(filepath)
        image = image.resize((224, 224))
        # Convert the PIL image to a NumPy array
        image = np.array(image)
        image = image.reshape(-1, 224, 224, 3)

        # Add a new axis to create a batch dimension
        # image = np.expand_dims(img_array, axis=0)
        #image_tensor = tf.convert_to_tensor(image)

        # model = tf.keras.applications.EfficientNetB1(weights="imagenet")
        model = tf.keras.models.load_model("efficientnetb0_model_toUse.h5")

        #print(image_tensor.shape)

        # Make predictions
        predictions = model.predict(image)

        # Decode the predictions
        predicted_classes = np.argmax(predictions, axis=1)
        classes = ['diarrhoea', 'lack of water in stool', 'normal stool', 'soft stool']

        # Print the predicted class
        print("Predicted class:", classes[predicted_classes[0]])

        # Placeholder for actual prediction logic
        final_pred_class = classes[predicted_classes[0]]
        predicted_bowel_health = 0
        if final_pred_class == 'normal stool':
            predicted_bowel_health = 100  
        elif final_pred_class == 'lack of water in stool':
            predicted_bowel_health = 75  
        elif final_pred_class == 'soft stool':
            predicted_bowel_health = 50  
        elif final_pred_class == 'diarrhoea':
            predicted_bowel_health = 25
        session['condition'] = final_pred_class
        
        
        # Generate the URL for the uploaded image
        image_url = url_for('uploaded_file', filename=filename)
        
        # Render the diagnosis page with the image and prediction
        return render_template('diagnose.html', bowel_health=predicted_bowel_health, image_url=image_url)
# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/chat', methods=['GET','POST'])
def generate_text():
    
    breed = session.get('breed_type', 'Unknown')
    age = session.get('age_dog', 'Unknown')
    cond = session.get('condition', 'Unknown')
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": f"My pet dog is a {age} year old {breed}. Their feces image indicates that they have {cond}. What do you recommend is the best course of action?"}
        ]
    )

    answer = completion.choices[0].message.content.strip()
    question = f"My pet dog is a {age} year old {breed}. Their stool indicates that they have {cond}. What do you recommend is the best course of action?"

    return render_template('chat.html', question=question, answer=answer)
if __name__ == '__main__':
    app.run(port=4000, debug=True)

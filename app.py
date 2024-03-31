from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
import gradio as gr
import os
import threading
from openai import OpenAI
# Flask configuration and initial setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

client = OpenAI(
    # Replace with your valid API key
    api_key=""
)



@app.route('/')
def home():
    # No image to display initially
    return render_template('home.html', image_url=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
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
        
        # Pass the URL for the saved image back to the template
        image_url = url_for('uploaded_file', filename=filename)
        return render_template('home.html', image_url=image_url)

@app.route('/diagnosis', methods=['POST'])
def diagnose():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
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
        #pass that image into test fn
        #get the result class
        #if class = dia:
        # display go to vet do this do that
        # Here, you would ideally use the saved image to run your model and predict bowel health
        predicted_bowel_health = 80  # Placeholder for actual prediction logic
        
        # Generate the URL for the uploaded image
        image_url = url_for('uploaded_file', filename=filename)
        
        # Render the diagnosis page with the image and prediction
        return render_template('diagnose.html', bowel_health=predicted_bowel_health, image_url=image_url)
# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

'''
@app.route('/chat', methods=['POST'])
def chatnow():
    breed='lab'
    age=2
    cond='diarrhea'
    return render_template('chat.html', dog_breed=breed, dog_age=age, dog_condition=cond)
'''
@app.route('/chat', methods=['GET','POST'])
def generate_text():
    breed = 'labrador'
    age = 8
    cond = 'excessive nonstop severe case of diarrhea'
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"My pet dog is a {age} year old {breed}. Her stool indicates that she has {cond}. What do you recommend is the best course of action?"}
        ]
    )

    answer = completion.choices[0].message.content.strip()
    question = f"My pet dog is a {age} year old {breed}. Her stool indicates that she has {cond}. What do you recommend is the best course of action?"

    return render_template('chat.html', question=question, answer=answer)
if __name__ == '__main__':
    app.run(port=4000, debug=True)

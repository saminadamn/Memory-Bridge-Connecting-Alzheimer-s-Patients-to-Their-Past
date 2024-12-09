
#PDF TO STORY GENERATION WITH AUDIO
# -- coding: utf-8 –
import os
from flask import Flask, request, render_template, make_response, jsonify
import threading
from gtts import gTTS
import gradio as gr
import fitz  # PyMuPDF
from transformers import pipeline
import tensorflow as tf

# Setting TensorFlow environment variable to disable oneDNN custom operations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Flask setup
app = Flask(_name_)
app.config["UPLOAD_FOLDER"] = "./uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs("static", exist_ok=True)

# Load local NLP model
story_generator = pipeline('text-generation', model='gpt2')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extracts text from the uploaded PDF file."""
    text = ""
    with fitz.open(pdf_file.name) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to generate a story using local NLP model
def generate_story(text, question):
    """Generates a story based on the extracted text using a local NLP model."""
    prompt = f"Based on the following text, answer the question: {question}\n\nText: {text}\n\nAnswer:"
    response = story_generator(prompt, max_new_tokens=150, truncation=True)
    return response[0]['generated_text']

# Function to generate audio using gTTS
def generate_audio(text, language="en"):
    try:
        tts = gTTS(text=text, lang=language)
        audio_path = os.path.join("static", "output_audio.mp3")
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        return f"Error generating audio: {e}"

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        prompt = request.form['prompt']
        question = request.form['question']
        story = generate_story(prompt, question)
        if "Error" in story:
            return make_response(jsonify({"error": story}), 500)
        audio_file = generate_audio(story)
        return render_template('result.html', story=story, audio_file=audio_file)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        file = request.files['file']
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        return make_response(jsonify({"message": "File uploaded successfully!"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Gradio interface function
def memory_interface(pdf_file, question):
    text = extract_text_from_pdf(pdf_file)
    story = generate_story(text, question)
    if "Error" in story:
        return story, None
    audio_file = generate_audio(story)
    return story, audio_file

# Gradio Interface Setup
iface = gr.Interface(
    fn=memory_interface,
    inputs=[
        gr.File(label="Upload PDF"),
        gr.Textbox(label="Ask a Question")
    ],
    outputs=[gr.Textbox(label="Generated Story"), gr.Audio(label="Generated Audio")],
    title="Interactive QA Bot",
    description="Upload a PDF document, ask questions, and receive answers based on the document content."
)

# Function to launch Gradio
def launch_gradio():
    print("Launching Gradio interface...")
    iface.launch(share=True)

# Function to run Flask app
def run_flask():
    print("Running Flask application...")
    app.run(debug=True, port=5000)

# Main execution
if _name_ == "_main_":
    flask_thread = threading.Thread(target=run_flask)
    gradio_thread = threading.Thread(target=launch_gradio)

    flask_thread.start()
    gradio_thread.start()

    flask_thread.join()
    gradio_thread.join()

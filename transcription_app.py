#AUDIO TRANSCRIPTION TO PDF FILE 
from flask import Flask, request, render_template_string, url_for
import os
from fpdf import FPDF
import gradio as gr
import time
import assemblyai as aai

app = Flask(_name_)
app.config["UPLOAD_FOLDER"] = "static"

# AssemblyAI API key
aai.settings.api_key = "6018d32b8d544f4295a5de66ad74a9e8"

# HTML template for the Flask interface
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AssemblyAI Transcription</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">AssemblyAI Transcription</h1>
        <form action="/" method="post" enctype="multipart/form-data" class="mt-4">
            <div class="form-group">
                <label for="language">Language:</label>
                <input type="text" class="form-control" id="language" name="language" required>
            </div>
            <div class="form-group">
                <label for="file">Upload your audio file:</label>
                <input type="file" class="form-control" id="file" name="file" accept="audio/*" required>
            </div>
            <button type="submit" class="btn btn-primary">Transcribe</button>
        </form>
        {% if transcription %}
        <div class="mt-4">
            <h2>Transcription</h2>
            <p>{{ transcription }}</p>
            <a href="{{ pdf_url }}" class="btn btn-success">Download Transcription as PDF</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

def transcribe_audio(file_path, speaker_labels=False):
    """Transcribe the given audio file using AssemblyAI."""
    config = aai.TranscriptionConfig(speaker_labels=speaker_labels)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        return f"Transcription failed: {transcript.error}"
    else:
        if speaker_labels:
            return "\n".join([f"Speaker {u.speaker}: {u.text}" for u in transcript.utterances])
        return transcript.text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    transcription = None
    pdf_url = None
    if request.method == 'POST':
        language = request.form['language']
        file = request.files['file']
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Transcribe audio using AssemblyAI
            transcription = transcribe_audio(file_path, speaker_labels=True)

            # Save transcription to a PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, transcription)
            output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], "transcription.pdf")
            pdf.output(output_pdf)
            pdf_url = url_for('static', filename="transcription.pdf")

    return render_template_string(html_template, transcription=transcription, pdf_url=pdf_url)

def transcribe_and_save(audio):
    # Save audio to a temporary file
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp_audio.wav")
    audio.save(audio_path)

    # Transcribe the audio file
    transcription = transcribe_audio(audio_path, speaker_labels=True)

    # Save transcription to a PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, transcription)
    output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], "transcription.pdf")
    pdf.output(output_pdf)

    return output_pdf

gr_interface = gr.Interface(
    fn=transcribe_and_save,
    inputs=gr.Audio(type="filepath"),  # Allow file upload for audio input
    outputs=gr.File(label="Download Transcription as PDF"),
    title="AssemblyAI Transcription to PDF",
    description="Upload an audio file to transcribe it into text and save it as a PDF."
)

@app.route('/gradio')
def gradio():
    return gr_interface.launch(share=False)

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000, debug=True)


# Memory-Bridge-Connecting-Alzheimer-s-Patients-to-Their-Past
# Audio Transcription, PDF Story Generation, and Memory Bridge Repository

This repository contains two projects:
1. Audio transcription to PDF file using AssemblyAI.
2. PDF-to-story generation with audio output using NLP and TTS.

## Repository Structure
```
.
├── app/                    # Source code for Flask applications
│   ├── transcription_app.py   # Audio transcription to PDF
│   ├── story_gen_app.py       # PDF-to-story generation
├── requirements.txt       # Python dependencies
├── static/                # Folder for static files (audio, PDF outputs)
├── templates/             # HTML templates for Flask apps
├── README.md              # Documentation
```

## Prerequisites
Ensure you have the following installed:
1. Python 3.8+
2. pip (Python package installer)

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/saminadamn/Memory-Bridge-Connecting-Alzheimer-s-Patients-to-Their-Past.git
   cd Memory-Bridge-Connecting-Alzheimer-s-Patients-to-Their-Past
   ```
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Audio Transcription to PDF
1. Navigate to the `app/` directory:
   ```
   cd app
   ```
2. Run the Flask app for transcription:
   ```
   python transcription_app.py
   ```
3. Open your browser and visit `http://localhost:5000`.
4. Upload your audio file and specify the language to receive transcription and download the PDF.



### PDF-to-Story Generation with Audio
1. Run the Flask app for story generation:
   ```
   python story_gen_app.py
   ```
2. Open your browser and visit `http://localhost:5000`.
3. Upload a PDF, ask a question, and receive a generated story with audio.
Upload personalized content (e.g., old letters, photos, or recordings) to create stories. 
Generate audio narrations to aid memory recollection and create a soothing, familiar experience.

#### How It Works
The core of our system lies in generating personalized stories. Upon receiving a prompt, our system processes the patient's input, retrieves the relevant content from the saved PDFs, and constructs a narrative based on the extracted information. The Gemini model ensures the generated story is not only accurate but also engaging for the patient.

To make the experience more immersive, we use the gTTS library to convert the generated text story into an audio file. This text-to-speech conversion allows patients to listen to their stories, providing an audio narration that is both comforting and reminiscent of the original recording.

Our platform is built using Flask, providing a user-friendly web interface for patients to upload recordings, input prompts, and access their generated stories. Additionally, we integrate Gradio to offer an interactive interface, allowing patients to upload PDFs and generate stories with ease.

With Memory Bridge, Alzheimer's patients can effortlessly relive their important moments, enhancing their emotional well-being and cognitive engagement. Experience the power of memories with Memory Bridge.

## Dependencies
The dependencies are listed in `requirements.txt` and include:
- Flask
- FPDF
- Gradio
- gTTS
- PyMuPDF
- transformers
- AssemblyAI Python SDK

To install dependencies, use:
```bash
pip install -r requirements.txt
```

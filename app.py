from flask import Flask, request, render_template_string
import speech_recognition as sr
import os
import tempfile

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Speech Recognition</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
            width: 400px;
            text-align: center;
        }
        h2 {
            color: #333;
            margin-bottom: 20px;
        }
        form {
            margin-top: 20px;
        }
        input[type="file"] {
            margin: 15px 0;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        input[type="submit"] {
            background: #6a11cb;
            background: linear-gradient(to right, #2575fc, #6a11cb);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s, background 0.3s;
        }
        input[type="submit"]:hover {
            transform: scale(1.05);
            background: linear-gradient(to right, #6a11cb, #2575fc);
        }
        .result {
            margin-top: 25px;
            padding: 15px;
            border-radius: 10px;
            background: #f9f9f9;
            box-shadow: inset 0px 2px 5px rgba(0,0,0,0.1);
            font-size: 16px;
            color: #444;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Upload Audio File</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="audio_file" accept=".wav,.aiff,.aifc,.flac" required>
            <br>
            <input type="submit" value="Upload & Transcribe">
        </form>
        {% if transcription %}
            <div class="result">
                <h3>Transcription:</h3>
                <p>{{ transcription }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def transcribe():
    transcription = None

    if request.method == "POST":
        if "audio_file" not in request.files:
            return "No file uploaded", 400

        file = request.files["audio_file"]
        if file.filename == "":
            return "No selected file", 400

        # Check extension
        allowed = ["wav", "aiff", "aifc", "flac"]
        ext = file.filename.split('.')[-1].lower()
        if ext not in allowed:
            return f"Unsupported file format. Please upload WAV, AIFF, or FLAC.", 400

        # Save temporarily
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        # Transcribe
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(file_path) as source:
                audio_data = recognizer.record(source)
                transcription = recognizer.recognize_google(audio_data)
        except Exception as e:
            transcription = f"Error transcribing audio: {e}"

    return render_template_string(HTML_TEMPLATE, transcription=transcription)

if __name__ == "__main__":
    app.run(debug=True)

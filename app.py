from flask import Flask, request, jsonify
from werkzeug.urls import url_quote
import librosa

app = Flask(__name__)

@app.route('/analyze_sound', methods=['POST'])
def analyze_sound():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Load the sound data
    sound_data, sample_rate = librosa.load(file, sr=None)

    # Get the duration of the sound in seconds
    duration = librosa.get_duration(y=sound_data, sr=sample_rate)

    # Get the number of samples in the sound
    num_samples = len(sound_data)

    # Get the number of channels (mono or stereo)
    num_channels = 1 if len(sound_data.shape) == 1 else sound_data.shape[0]

    # Get the sample rate
    sample_rate_hz = sample_rate

    # Return the sound details
    return jsonify({
        'duration_seconds': duration,
        'num_samples': num_samples,
        'num_channels': num_channels,
        'sample_rate_hz': sample_rate_hz
    }), 200


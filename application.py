from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
# from src.pipeline.generate_pipeline import GenerationPipeline

application = Flask(__name__)
app = application

MIDI_FILE_PATH = 'artifacts/test_output.mid'


# Route to serve the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route to serve MIDI files
@app.route('/midi/<filename>')
def get_midi(filename):
    return send_from_directory('artifacts',MIDI_FILE_PATH)

# Simulate generating a new MIDI file
@app.route('/generate', methods=['POST'])
def generate_midi():
    # pipeline = GenerationPipeline()
    # midi_file = pipeline.generate_music()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

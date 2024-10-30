from flask import Flask, render_template, request, send_file, url_for, flash, redirect
import os
from src.pipeline.generate_pipeline import GenerationPipeline

application = Flask(__name__)
app = application

# Path where the MIDI file will be saved
MIDI_FILE_PATH = 'artifacts/test_output.mid'
app.secret_key = 'your_secret_key'  # For flashing messages

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        generate_midi()
        flash("Music generated successfully! Scroll down to download your file.")
    return render_template('home.html', midi_exists=os.path.exists(MIDI_FILE_PATH))


def generate_midi():
    """Function to generate the MIDI file using your pipeline."""
    # Uncomment the following to use your actual pipeline:
    pipeline = GenerationPipeline()
    pipeline.generate_music()

    # Simulating the music generation for now.
    with open(MIDI_FILE_PATH, 'w') as f:
        f.write('Simulated MIDI content.')  # Placeholder content

    print("Music generated and saved at:", MIDI_FILE_PATH)


@app.route('/download')
def download_file():
    """Sends the MIDI file for download."""
    if os.path.exists(MIDI_FILE_PATH):
        return send_file(MIDI_FILE_PATH, as_attachment=True)
    else:
        flash("File not found!")
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

import subprocess
import sys

# This code is to ensure that the require flask python libararies are installed
# If the libraries are not installed, theyll be installed by this snippet of code

def install_flask(): 
    try:
        import flask
    except ImportError:
        subprocess.call(['pip', 'install', 'flask'])

install_flask()
 
#import required Flask Libraries
from flask import Flask, render_template, request, jsonify

#import Detection and Correction Programs
from Detection import analyze_gender
from Correction import process_text
from Feedback import append_feedback_to_csv

# Main Program
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    text = request.json.get('text')
    csv_file = 'data/Corrected_Language.csv'
    percentages = analyze_gender(text, csv_file)  # This returns a dict with Male, Female, Neutral
    return jsonify({
        'labels': ['Male', 'Female', 'Neutral'],  # Fixed order
        'datasets': [{'data': [percentages['Male'], percentages['Female'], percentages['Neutral']]}]  # Correctly ordered data
    })

@app.route('/convert/<gender>', methods=['POST'])
def convert(gender):
    text = request.json.get('text')
    csv_file = 'data/Corrected_Language.csv'
    converted_text = process_text(text, csv_file, gender)  # Call the process_text function
    return jsonify({'converted_text': converted_text})  # Return the modified text

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Check if all fields are provided
        if not name or not email or not message:
            return jsonify({'status': 'error', 'message': 'All fields are required!'}), 400

        # Call the function to append feedback to the CSV file
        append_feedback_to_csv(name, email, message)

        # Return a success response
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
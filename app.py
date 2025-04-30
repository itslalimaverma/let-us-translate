from flask import Flask, render_template, request
import requests, os, uuid, json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Route for GET method (initial form page)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route for POST method (form submission to translate text)
@app.route('/', methods=['POST'])
def index_post():
    # Get text and language from form
    original_text = request.form['text']
    target_language = request.form['language']

    # Get API details from environment variables
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Azure Translator API setup
    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language
    constructed_url = endpoint + path + target_language_parameter

    # Headers for API request
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Request body with original text
    body = [{ 'text': original_text }]

    # Call Azure Translator API
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    translator_response = translator_request.json()

    # Extract translated text
    translated_text = translator_response[0]['translations'][0]['text']

    # Show results page
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

if __name__ == '__main__':
    app.run(debug=True)

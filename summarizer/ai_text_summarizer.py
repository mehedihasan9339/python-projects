# ai_text_summarizer.py
from flask import Flask, request, jsonify
from transformers import pipeline

# Initialize Flask app
app = Flask(__name__)

# Load the summarization model
summarizer = pipeline("summarization")

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return jsonify({"summary": summary[0]['summary_text']})

# Function to run the Flask app
def run_app():
    app.run(debug=True)

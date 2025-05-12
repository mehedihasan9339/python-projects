from flask import Flask, request, jsonify
from transformers import pipeline, BartTokenizer

# Initialize Flask app and summarizer
app = Flask(__name__)
summarizer = pipeline("summarization", model="facebook/bart-large-xsum")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-xsum")

MAX_TOKENS = 1024  # Max tokens supported by the model

def chunk_text(input_text):
    # Tokenize the input text and split it into chunks based on token limit
    tokens = tokenizer.encode(input_text)
    # Create chunks with the max number of tokens that the model can handle
    chunks = [tokens[i:i + MAX_TOKENS] for i in range(0, len(tokens), MAX_TOKENS)]
    return chunks

@app.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.get_json()

    # Validate input
    if not data or "text" not in data:
        return jsonify({"error": "Please provide text in the request body."}), 400

    input_text = data["text"]

    # Check for empty input text
    if not input_text.strip():
        return jsonify({"error": "Text is empty."}), 400

    # Tokenize and chunk the input text if it's too long
    chunks = chunk_text(input_text)
    
    summaries = []
    for chunk in chunks:
        try:
            # Decode the tokenized chunk back into text
            chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
            # Summarize the chunk
            summary = summarizer(chunk_text, max_length=130, min_length=30, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            return jsonify({"error": f"Error summarizing chunk: {str(e)}"}), 500
    
    # Combine all summaries into one
    return jsonify({"summary": " ".join(summaries)})

@app.route("/", methods=["GET"])
def home():
    return "Text Summarization API is running!"

if __name__ == "__main__":
    app.run(debug=True)

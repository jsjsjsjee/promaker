from flask import Flask, request, jsonify, render_template
import wikipediaapi

app = Flask(__name__)

def fetch_wikipedia_data(topic):
    """Fetches detailed information and images about a topic from Wikipedia."""
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(topic)
    
    if not page.exists():
        return {"text": "No information found.", "images": []}
    
    # Extract text and images
    text = page.text[:5000]  # Limit to 5000 characters
    images = [img for img in page.images if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return {"text": text, "images": images[:5]}  # Limit to 5 images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    topic = request.args.get('topic', '')
    if not topic:
        return jsonify({"error": "No topic provided."}), 400
    
    data = fetch_wikipedia_data(topic)
    return jsonify(data)

if __name__ == '_main_':
    app.run(debug=True)
from flask import Flask, request, jsonify
import sys
sys.path.insert(0, '/home/debianuser/ai_devsecops/ai_labs/devsecops_ai_lab')
from src.models.bert_classifier import BertClassifier

app = Flask(__name__)
classifier = BertClassifier()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    result = classifier.predict(text)
    return jsonify(result), 200

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    data = request.get_json()
    texts = data.get('texts', [])
    
    if not texts:
        return jsonify({"error": "No texts provided"}), 400
    
    results = classifier.batch_predict(texts)
    return jsonify({"predictions": results}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

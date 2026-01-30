from transformers import pipeline

class BertClassifier:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        """Initialize BERT classifier - downloads model on first use"""
        self.model_name = model_name
        self.classifier = pipeline("sentiment-analysis", model=model_name)
    
    def predict(self, text):
        """Predict sentiment for given text"""
        result = self.classifier(text)
        return {
            "text": text,
            "label": result[0]["label"],
            "score": round(result[0]["score"], 4)
        }
    
    def batch_predict(self, texts):
        """Predict sentiment for multiple texts"""
        return [self.predict(text) for text in texts]

import pytest
import sys
sys.path.insert(0, '/home/debianuser/ai_devsecops/ai_labs/devsecops_ai_lab')
from src.models.bert_classifier import BertClassifier

@pytest.fixture
def classifier():
    return BertClassifier()

def test_predict_positive(classifier):
    result = classifier.predict("This movie is amazing!")
    assert "label" in result
    assert "score" in result
    assert result["label"] in ["POSITIVE", "NEGATIVE"]

def test_predict_negative(classifier):
    result = classifier.predict("This is terrible")
    assert "label" in result
    assert "score" in result

def test_batch_predict(classifier):
    texts = ["Great movie!", "Bad experience"]
    results = classifier.batch_predict(texts)
    assert len(results) == 2
    assert all("label" in r for r in results)

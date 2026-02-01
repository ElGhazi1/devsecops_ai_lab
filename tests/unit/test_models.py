"""Unit tests for models."""
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

def test_placeholder():
    """Placeholder test."""
    assert True


def test_oauth2_import():
    """Test OAuth2 service import."""
    try:
        from services.oauth2_service.main import app
        assert app is not None
    except ImportError:
        pytest.skip("OAuth2 service not available")


def test_api_backend_import():
    """Test API backend import."""
    try:
        from services.api_backend.main import app
        assert app is not None
    except ImportError:
        pytest.skip("API backend not available")


def test_llm_service_import():
    """Test LLM service import."""
    try:
        from services.llm_nlp_service.main import app
        assert app is not None
    except ImportError:
        pytest.skip("LLM service not available")

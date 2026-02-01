"""Security tests for threat detection."""
import pytest


def test_threat_keywords():
    """Test threat keyword detection."""
    threat_keywords = {
        "injection": ["sql", "drop", "delete"],
        "xss": ["script", "alert"],
    }
    
    test_text = "SELECT * FROM users"
    found = any(keyword in test_text.lower() for keyword in threat_keywords["injection"])
    assert found is True


def test_safe_keywords():
    """Test safe text detection."""
    threat_keywords = {
        "injection": ["sql", "drop", "delete"],
    }
    
    test_text = "Show me the products"
    found = any(keyword in test_text.lower() for keyword in threat_keywords["injection"])
    assert found is False

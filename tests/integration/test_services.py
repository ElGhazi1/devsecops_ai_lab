"""Integration tests for services."""
import pytest


@pytest.mark.skip(reason="Requires docker-compose running")
def test_oauth2_health():
    """Test OAuth2 service health."""
    import httpx
    response = httpx.get("http://localhost:8001/health")
    assert response.status_code == 200


@pytest.mark.skip(reason="Requires docker-compose running")
def test_api_backend_health():
    """Test API backend health."""
    import httpx
    response = httpx.get("http://localhost:8002/health")
    assert response.status_code == 200


@pytest.mark.skip(reason="Requires docker-compose running")
def test_llm_service_health():
    """Test LLM service health."""
    import httpx
    response = httpx.get("http://localhost:8003/health")
    assert response.status_code == 200

import pytest
from unittest.mock import MagicMock, patch
from tools.images import generate_images, DEFAULT_IMAGE

def test_images_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = generate_images("test")
    assert len(result) == 2
    assert result[0] == DEFAULT_IMAGE

def test_images_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    mock_part = MagicMock()
    mock_part.inline_data.data = b"imgbytes"
    mock_cand = MagicMock()
    mock_cand.content.parts = [mock_part]
    mock_response = MagicMock()
    mock_response.candidates = [mock_cand]
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    with patch("tools.images.genai.Client", return_value=mock_client):
        result = generate_images("test")
        assert len(result) == 1
        assert result[0] == "aW1nYnl0ZXM="

def test_images_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("fail")
    with patch("tools.images.genai.Client", return_value=mock_client):
        result = generate_images("test")
        assert result == [DEFAULT_IMAGE, DEFAULT_IMAGE]

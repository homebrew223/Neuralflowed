import pytest
from unittest.mock import MagicMock, patch
from tools.writer import write

def test_writer_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        write("test", [])

def test_writer_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    mock_response = MagicMock()
    mock_response.text = '{"headline":"Test","sections":[{"title":"A","body":"B"}],"cta_text":"C"}'
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    with patch("tools.writer.genai.Client", return_value=mock_client):
        result = write("test", [])
        assert result["headline"] == "Test"
        assert len(result["sections"]) == 1

def test_writer_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("API down")
    with patch("tools.writer.genai.Client", return_value=mock_client):
        result = write("test", [])
        assert "headline" in result

import pytest
from unittest.mock import MagicMock, patch
from tools.research import research

def test_research_missing_key(monkeypatch):
    monkeypatch.delenv("SERPER_API_KEY", raising=False)
    with pytest.raises(SystemExit) as exc_info:
        research("test")
    assert exc_info.value.code == 1

def test_research_success(monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "fake-key")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "organicResults": [
            {"title": "Title 1", "link": "http://a.com", "snippet": "Desc 1"},
            {"title": "Title 2", "link": "http://b.com", "snippet": "Desc 2"},
        ]
    }
    with patch("tools.research.requests.post", return_value=mock_resp):
        result = research("test", n=2)
        assert len(result) == 2
        assert result[0]["title"] == "Title 1"

def test_research_empty(monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "fake-key")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"organicResults": []}
    with patch("tools.research.requests.post", return_value=mock_resp):
        result = research("test")
        assert result == []

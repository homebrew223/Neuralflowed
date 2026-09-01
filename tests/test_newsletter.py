import pytest
from unittest.mock import patch
from tools.newsletter import main

def test_newsletter_imports():
    assert callable(main)

def test_newsletter_flow(monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "k")
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    monkeypatch.setenv("GMAIL_CLIENT_ID", "cid")
    monkeypatch.setenv("GMAIL_CLIENT_SECRET", "csec")
    monkeypatch.setenv("GMAIL_REFRESH_TOKEN", "rtok")
    with patch("tools.newsletter.research", return_value=[]), \
         patch("tools.newsletter.write", return_value={"headline":"H","sections":[],"cta_text":"C"}), \
         patch("tools.newsletter.generate_images", return_value=[]), \
         patch("tools.newsletter.format_email", return_value="<html></html>"), \
         patch("tools.newsletter.send", return_value=True) as mock_send:
        import sys
        sys.argv = ["newsletter", "--topic", "test", "--to", "a@b.com"]
        main()
        mock_send.assert_called_once()

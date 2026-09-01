import pytest
from unittest.mock import MagicMock, patch
from tools.sender import send

def test_sender_missing_creds(monkeypatch):
    monkeypatch.delenv("GMAIL_CLIENT_ID", raising=False)
    with pytest.raises(SystemExit):
        send("<html></html>")

def test_sender_success(monkeypatch):
    monkeypatch.setenv("GMAIL_CLIENT_ID", "cid")
    monkeypatch.setenv("GMAIL_CLIENT_SECRET", "csec")
    monkeypatch.setenv("GMAIL_REFRESH_TOKEN", "rtok")
    mock_creds = MagicMock()
    mock_service = MagicMock()
    mock_service.users().messages().send.return_value = MagicMock()
    with patch("tools.sender.Credentials", return_value=mock_creds), \
         patch("tools.sender.build", return_value=mock_service), \
         patch("tools.sender.MIMEMultipart") as MockMultipart, \
         patch("tools.sender.MIMEText"):
        mock_msg = MagicMock()
        mock_msg.as_bytes.return_value = b"raw"
        MockMultipart.return_value = mock_msg
        send("<html></html>", "to@example.com")
        mock_service.users().messages().send.assert_called_once()

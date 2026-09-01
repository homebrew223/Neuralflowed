import pytest
from tools.formatter import format_email

def test_formatter_has_headline():
    html = format_email("AI", {"headline":"Hello","sections":[],"cta_text":"Go"}, [])
    assert "Hello" in html
    assert "Simple" in html

def test_formatter_includes_base64_image():
    html = format_email("AI", {"headline":"H","sections":[],"cta_text":"Go"}, ["abc123"])
    assert "data:image/png;base64,abc123" in html
    assert "#C8202F" in html
    assert "#1A1A1A" in html

def test_formatter_has_sections():
    html = format_email("AI", {
        "headline":"H",
        "sections":[{"title":"A","body":"B"}],
        "cta_text":"Go"
    }, [])
    assert "A" in html
    assert "B" in html

def test_formatter_has_cta():
    html = format_email("AI", {"headline":"H","sections":[],"cta_text":"Click"}, [])
    assert "Click" in html
    assert "#C8202F" in html

# Newsletter Automation — Implementation Plan

**Spec:** `docs/superpowers/specs/2026-09-01-newsletter-automation-design.md`
**Approach:** Subagent-driven development — one fresh subagent per task, review after each.
**Trigger:** `python3 tools/newsletter.py --topic "X"`

## Task 1 — Scaffolding (foundation)
- Deliverables: `.env` (verify), `requirements.txt`, `tools/__init__.py`, `tests/__init__.py`
- Verify `.env` has the 5 key placeholders
- `requirements.txt`: requests, google-genai, google-api-python-client, google-auth-oauthlib, python-dotenv, pytest
- Create empty `__init__.py` files
- Commit

## Task 2 — Research tool (Serper)
- `tools/research.py`: function `research(topic: str) -> list[dict]` — calls Serper API, returns top-5 articles (title, url, snippet)
- Retry once on failure, raise clear error on missing key
- `tests/test_research.py`: mock-based tests — success returns 5 items, missing key exits 1, empty response handled
- Commit

## Task 3 — Writer tool (Gemini text)
- `tools/writer.py`: function `write(topic: str, articles: list[dict]) -> dict` — calls Gemini, returns {headline, sections:[{title, body}], cta_text}
- Fallback to editorial content if API fails
- `tests/test_writer.py`: mock tests — returns valid dict shape, fallback works
- Commit

## Task 4 — Images tool (Gemini Imagen)
- `tools/images.py`: function `generate_images(topic: str) -> list[str]` — calls Gemini Imagen/Nano, returns list of base64 PNG strings (2 images)
- Fallback to a styled placeholder div if generation fails
- `tests/test_images.py`: mock tests — returns 2 base64 strings, fallback returns placeholder
- Commit

## Task 5 — Formatter tool (HTML email)
- `tools/formatter.py`: function `format_email(topic: str, content: dict, images: list[str]) -> str` — builds single HTML email with inline CSS per brand spec, images as base64 `<img>`
- Brand colors, typography, layout from spec
- `tests/test_formatter.py`: verify HTML contains expected elements, inline styles, base64 images
- Commit

## Task 6 — Sender tool (Gmail API)
- `tools/sender.py`: function `send(html: str, to: str) -> bool` — sends HTML email via Gmail API using .env credentials
- Handles missing credentials gracefully
- `tests/test_sender.py`: mock tests — sends successfully, missing creds raises clear error
- Commit

## Task 7 — CLI orchestrator (newsletter.py)
- `tools/newsletter.py`: `argparse` CLI with `--topic`, `--to` flags; calls research -> write -> images -> format -> send in sequence
- Progress output to stdout, error handling at each step
- `tests/test_newsletter.py`: verify CLI parsing, end-to-end mocked flow
- Commit

## Task 8 — Workflow SOP
- `workflows/newsletter.md`: plain-language step-by-step SOP mirroring the tool chain, inputs/outputs, edge cases
- Commit

## Task 9 — Final review
- `.gitignore`: ignore .env, token.json, __pycache__, *.pyc, .tmp/
- Dry-run `python3 tools/newsletter.py --topic "test"` with mocked APIs (if possible) — verify imports resolve and CLI prints usage
- Final commit

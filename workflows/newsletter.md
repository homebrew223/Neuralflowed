# Newsletter Automation — Workflow SOP

## Objective
Build and send a branded HTML newsletter for a given topic, end to end, using the WAT tool chain.

## Trigger
`python3 tools/newsletter.py --topic "X" [--to email@example.com]`

## Inputs
- `--topic` — newsletter subject (required)
- `--to` — recipient email (optional, defaults to `me@example.com`)
- `.env` — API keys: `SERPER_API_KEY`, `GEMINI_API_KEY`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`

## Steps (Layer 3: Tools)
1. **Research** (`tools/research.py`) — `research(topic)` queries Serper API, returns top-5 articles (title, url, snippet). Retries once on failure. Exits 1 if `SERPER_API_KEY` is missing.
2. **Write** (`tools/writer.py`) — `write(topic, articles)` calls Gemini to produce `{headline, sections:[{title, body}], cta_text}`. Falls back to editorial content if the API is down.
3. **Images** (`tools/images.py`) — `generate_images(topic)` calls Gemini Imagen for 2 infographic images (base64 PNG). Falls back to placeholder images if generation fails or `GEMINI_API_KEY` is missing.
4. **Format** (`tools/formatter.py`) — `format_email(topic, content, images)` builds a single HTML email with inline CSS per the "Simple" brand spec. Header (black), hero image, H1, sections (image + text), CTA (red), footer (black). Images are `<img src="data:image/png;base64,...">`.
5. **Send** (`tools/sender.py`) — `send(html, to)` authenticates to Gmail via OAuth2 refresh token and sends the HTML email. Exits 1 if Gmail credentials are missing.

## Steps (Layer 2: Agent)
`tools/newsletter.py` orchestrates steps 1–5 in order, passing outputs forward:
`research -> write -> generate_images -> format_email -> send`

## Edge cases
- Missing API key → prints which key is missing, exits 1
- API call fails → retries once, then falls back to editorial content or placeholder images
- No articles found → writer still generates content (never empty email)
- Image generation fails → formatter renders placeholder blocks

## Outputs
- A single HTML email delivered to the recipient via Gmail API
- Console progress output at each step

## Error handling
- Each tool prints a clear message and either retries, falls back, or exits 1
- The orchestrator never crashes silently; every failure is reported to stdout

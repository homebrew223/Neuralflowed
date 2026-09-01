# Newsletter Automation — Design Spec

**Project:** Newsletter Automation CLI
**Framework:** WAT (Workflows, Agents, Tools)
**Trigger:** `python3 tools/newsletter.py --topic "X"` (on-demand)
**Stack:** Python 3, requests, google-genai, google-api-python-client, python-dotenv

## Objective
Build a single HTML email (inline styles, base64-embedded images) for a given topic, then deliver it via Gmail API.

## Architecture
- **Layer 1 (Workflow):** `workflows/newsletter.md` — step-by-step SOP
- **Layer 2 (Agent):** `tools/newsletter.py` — orchestrates sub-tools, handles errors
- **Layer 3 (Tools):**
  - `tools/research.py` — Serper API to top-5 articles (title, url, snippet)
  - `tools/writer.py` — Gemini to headline + 3 body sections + CTA text
  - `tools/images.py` — Gemini Imagen to 2 infographic images (base64)
  - `tools/formatter.py` — Builds branded HTML email from section data + images
  - `tools/sender.py` — Gmail API to sends HTML email to a configured recipient

## Brand ("Simple")
- Palette: #1A1A1A, #C8202F, #7A1620, #4D4D4D, #F4F3F1, #FFFFFF
- Layout: Header(black, logo+date) to Hero to Sections(image+text) to CTA(red) to Footer(black)
- Typography: H1 40-60px Bold, H2 20-28px Bold(last word red), body 11-13px line-height 1.5
- Ratio: ~60% off-white/white, ~25% black, ~15% red accent
- Logo: full lockup on light bg (red icon + #1A1A1A wordmark), reversed on dark

## Output format
Single HTML file with all images base64-encoded inline (`<img src="data:image/png;base64,...">`),
inline CSS per brand spec. Sent as HTML email via Gmail API.

## Error handling
- Missing API key -> print which key is missing, exit 1
- API call fails -> retry once, then skip that section and continue
- No articles found -> generate editorial content anyway (never empty email)

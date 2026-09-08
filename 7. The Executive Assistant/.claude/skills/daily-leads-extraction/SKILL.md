# Daily Leads Extraction

## Purpose
Systematically find and extract high-intent leads for StrideAhead's AI automation services.

## When to Use
Run daily or on-demand when Jesse or Badger needs fresh leads for outreach.

## Workflow

### 1. Define Lead Criteria
Before searching, confirm:
- **Industry/niche** (e.g., SaaS, ecommerce, agencies, real estate)
- **Company size** (employees, revenue range)
- **Pain points** that AI automation solves (manual processes, scaling issues, repetitive tasks)
- **Budget signal** (funded startups, growing companies, established businesses)

### 2. Source Leads From
Pick sources based on what's available and working:
- **Upwork** — Search for automation/AI-related job postings, filter by budget and recency
- **LinkedIn** — Search for decision makers (founders, ops leads, CMOs) in target niches
- **Google** — Search for companies posting about automation needs, hiring for ops roles
- **Twitter/X** — Look for people complaining about manual processes or asking for automation help
- **Industry directories** — Crunchbase, Clutch, G2 for companies in target verticals

### 3. Extract Lead Data
For each lead, capture:
- **Company name**
- **Contact name + title**
- **Email** (if available)
- **LinkedIn URL**
- **Phone** (if available)
- **Source** (where you found them)
- **Signal** (why they're a good lead — what pain point did they show?)
- **Intent level** (Hot / Warm / Cold)

### 4. Qualify
Score each lead:
- **Hot** — Actively looking for automation, has budget, decision maker identified
- **Warm** — Shows pain signals, not actively searching yet
- **Cold** — Fits the profile but no immediate signal

### 5. Output
Save qualified leads to a file in `projects/leads/` with format:
```
leads-YYYY-MM-DD.md
```

File structure:
```markdown
# Leads — [Date]

## Hot Leads
| Company | Contact | Title | Email | Signal | Source |

## Warm Leads
| Company | Contact | Title | Email | Signal | Source |

## Cold Leads
| Company | Contact | Title | Email | Signal | Source |
```

### 6. Hand Off
- Notify Jesse of hot leads immediately
- Queue warm leads for outreach prep
- Cold leads go into the pipeline for later

## Tips
- Quality over quantity — 10 good leads beat 100 junk ones
- Look for recent signals (job posts from last 7 days, social posts from last 30 days)
- Track what sources produce the best leads over time
- Update lead criteria as StrideAhead's ideal client profile evolves

## Files
- Output directory: `projects/leads/`
- Lead criteria: `context/work.md` (update ideal client profile there)
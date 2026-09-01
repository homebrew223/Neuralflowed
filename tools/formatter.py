import os
from datetime import datetime

DEFAULT_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

def _img_tag(src: str, style: str = "") -> str:
    return f'<img src="data:image/png;base64,{src}" style="{style}" alt="">'

def format_email(topic: str, content: dict, images: list[str]) -> str:
    headline = content.get("headline", topic)
    sections = content.get("sections", [])
    cta_text = content.get("cta_text", "Read more")
    hero_src = images[0] if images else DEFAULT_IMAGE
    date = datetime.now().strftime("%B %d, %Y")

    section_rows = ""
    for i, sec in enumerate(sections):
        title = sec.get("title", "")
        body = sec.get("body", "")
        img_src = images[i + 1] if i + 1 < len(images) else None
        if img_src:
            cells = (
                f'<td valign="top" width="280" style="padding:10px;">'
                f'{_img_tag(img_src, "width:100%;height:auto;display:block;")}'
                f'</td>'
                f'<td valign="top" style="padding:10px;">'
            )
        else:
            cells = (
                f'<td valign="top" style="padding:10px;">'
            )
        cells += (
            f'<h2 style="margin:0 0 8px 0;font-size:22px;font-weight:bold;color:#1A1A1A;font-family:\'Helvetica Neue\',Arial,sans-serif;">'
            f'{title}</h2>'
            f'<p style="margin:0 0 12px 0;font-size:13px;line-height:1.5;color:#333;font-family:Arial,sans-serif;">'
            f'{body}</p>'
            f'</td>'
        )
        section_rows += f"<tr>{cells}</tr>"

    sections_html = f'<table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;margin:0 auto;">{section_rows}</table>'

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#F4F3F1;font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#1A1A1A" style="max-width:600px;margin:0 auto;">
<tr>
<td style="color:#FFFFFF;font-size:26px;font-weight:bold;padding:24px 20px;">Simple</td>
<td style="color:#888;font-size:12px;text-align:right;padding:24px 20px;">{date}</td>
</tr>
</table>
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;margin:0 auto;">
<tr><td style="padding:0;">{_img_tag(hero_src, "width:100%;height:auto;display:block;")}</td></tr>
<tr><td style="padding:24px 20px 0 20px;">
<h1 style="margin:0 0 12px 0;font-size:42px;font-weight:bold;color:#1A1A1A;line-height:1.15;">{headline}</h1>
</td></tr>
</table>
{sections_html}
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;margin:0 auto;">
<tr><td style="padding:8px 20px 24px 20px;text-align:center;">
<a href="#" style="display:inline-block;background:#C8202F;color:#FFFFFF;font-size:14px;font-weight:bold;padding:14px 32px;border-radius:6px;text-decoration:none;">{cta_text}</a>
</td></tr>
</table>
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#1A1A1A" style="max-width:600px;margin:0 auto;">
<tr><td style="padding:24px 20px;color:#FFFFFF;font-size:11px;line-height:1.5;text-align:center;">
<div style="color:#C8202F;font-size:16px;font-weight:bold;margin-bottom:8px;">Simple</div>
<div>Newsletter &middot; {topic}</div>
</td></tr>
</table>
</body>
</html>"""

from datetime import datetime
from html import escape
from pathlib import Path


def write_daily_report(report_path, items, summary):
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# AI Intelligence Daily Report",
        "",
        f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Summary",
        "",
        summary,
        "",
        "## Items",
        "",
    ]

    if not items:
        lines.append("No relevant items found.")
    else:
        for item in items:
            lines.extend([
                f"### {item.get('title', 'Untitled')}",
                "",
                f"- Source: {item.get('source', '')}",
                f"- Category: {item.get('category', 'general_ai')}",
                f"- Published: {item.get('published', '')}",
                f"- URL: {item.get('url', '')}",
                "",
                item.get("summary", "").strip(),
                "",
            ])

    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_html_report(report_path, items, summary):
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    cards = []
    if not items:
        cards.append('<article class="empty">No relevant items found.</article>')
    else:
        for item in items:
            title = escape(item.get("title", "Untitled"))
            source = escape(item.get("source", ""))
            category = escape(item.get("category", "general_ai").replace("_", " ").title())
            published = escape(item.get("published", ""))
            url = escape(item.get("url", ""), quote=True)
            item_summary = escape(item.get("summary", "").strip())
            link = f'<a href="{url}" target="_blank" rel="noopener">Open source</a>' if url else ""
            cards.append(f"""
<article class="card">
  <div class="meta"><span>{category}</span><span>{source}</span></div>
  <h2>{title}</h2>
  <p>{item_summary}</p>
  <footer><span>{published}</span>{link}</footer>
</article>""")

    html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Intelligence Radar</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f9;
      --text: #17202a;
      --muted: #637083;
      --line: #dbe1e8;
      --card: #ffffff;
      --accent: #0f766e;
      --accent-soft: #d9f3ef;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); line-height: 1.55; }}
    header {{ padding: 28px 18px 18px; background: #ffffff; border-bottom: 1px solid var(--line); }}
    main, .brand {{ width: min(880px, 100%); margin: 0 auto; }}
    main {{ padding: 18px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; line-height: 1.15; letter-spacing: 0; }}
    .summary {{ margin: 0; color: var(--muted); font-size: 15px; }}
    .stats {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin: 18px 0; }}
    .stat {{ padding: 14px; border: 1px solid var(--line); background: var(--card); border-radius: 8px; }}
    .stat strong {{ display: block; font-size: 24px; line-height: 1.2; }}
    .stat span {{ color: var(--muted); font-size: 13px; }}
    .card, .empty {{ margin: 12px 0; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: var(--card); }}
    .meta {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; color: var(--accent); font-size: 12px; font-weight: 700; text-transform: uppercase; }}
    .meta span {{ padding: 4px 8px; border-radius: 999px; background: var(--accent-soft); }}
    h2 {{ margin: 0 0 10px; font-size: 19px; line-height: 1.25; letter-spacing: 0; }}
    p {{ margin: 0 0 12px; }}
    footer {{ display: flex; justify-content: space-between; gap: 12px; align-items: center; color: var(--muted); font-size: 13px; border-top: 1px solid var(--line); padding-top: 12px; }}
    a {{ color: var(--accent); font-weight: 700; text-decoration: none; white-space: nowrap; }}
    @media (max-width: 560px) {{
      header {{ padding-top: 22px; }}
      h1 {{ font-size: 24px; }}
      main {{ padding: 12px; }}
      .stats {{ grid-template-columns: 1fr; }}
      footer {{ align-items: flex-start; flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <h1>AI Intelligence Radar</h1>
      <p class="summary">{escape(summary)} Updated {escape(generated_at)}.</p>
    </div>
  </header>
  <main>
    <section class="stats" aria-label="Report stats">
      <div class="stat"><strong>{len(items)}</strong><span>Relevant items</span></div>
      <div class="stat"><strong>{len(set(item.get('source', '') for item in items))}</strong><span>Sources</span></div>
    </section>
    {''.join(cards)}
  </main>
</body>
</html>
"""
    report_path.write_text(html, encoding="utf-8")

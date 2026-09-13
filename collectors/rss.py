import re
from datetime import datetime, timezone
from html import unescape

import feedparser


def clean_text(value):
    text = unescape(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def collect_rss(feed_urls, max_items=5):
    items = []
    for feed_url in feed_urls:
        parsed = feedparser.parse(feed_url)
        source_name = parsed.feed.get("title", feed_url)

        for entry in parsed.entries[:max_items]:
            items.append({
                "source": clean_text(source_name),
                "title": clean_text(entry.get("title", "Untitled")),
                "url": entry.get("link", ""),
                "published": clean_text(entry.get("published", "")),
                "summary": clean_text(entry.get("summary", "")),
                "collected_at": datetime.now(timezone.utc).isoformat(),
            })
    return items

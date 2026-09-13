from datetime import datetime, timezone

import feedparser


def collect_rss(feed_urls, max_items=5):
    items = []
    for feed_url in feed_urls:
        parsed = feedparser.parse(feed_url)
        source_name = parsed.feed.get("title", feed_url)

        for entry in parsed.entries[:max_items]:
            items.append({
                "source": source_name,
                "title": entry.get("title", "Untitled"),
                "url": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "collected_at": datetime.now(timezone.utc).isoformat(),
            })
    return items

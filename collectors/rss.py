import email.utils
import re
from datetime import datetime, timedelta, timezone
from html import unescape

import feedparser


def clean_text(value):
    text = unescape(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_entry_date(entry):
    raw_date = entry.get("published") or entry.get("updated") or ""
    if not raw_date:
        return None, ""

    try:
        parsed = email.utils.parsedate_to_datetime(raw_date)
    except Exception:
        return None, clean_text(raw_date)

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    parsed = parsed.astimezone(timezone.utc)
    return parsed, clean_text(raw_date)


def collect_rss(feed_urls, max_items=10, recent_days=7, max_total_items=30):
    cutoff = datetime.now(timezone.utc) - timedelta(days=recent_days)
    items = []

    for feed_url in feed_urls:
        parsed = feedparser.parse(feed_url)
        source_name = parsed.feed.get("title", feed_url)
        kept_for_source = 0

        for entry in parsed.entries:
            published_at, published_text = parse_entry_date(entry)
            if published_at is None or published_at < cutoff:
                continue
            if kept_for_source >= max_items:
                break

            items.append({
                "source": clean_text(source_name),
                "title": clean_text(entry.get("title", "Untitled")),
                "url": entry.get("link", ""),
                "published": published_text,
                "published_at": published_at.isoformat(),
                "summary": clean_text(entry.get("summary", "")),
                "collected_at": datetime.now(timezone.utc).isoformat(),
            })
            kept_for_source += 1

    items.sort(key=lambda item: item.get("published_at", ""), reverse=True)
    return items[:max_total_items]

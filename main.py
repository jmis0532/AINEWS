from pathlib import Path

import yaml
from dotenv import load_dotenv

from collectors.rss import collect_rss
from ai.filter import filter_items
from ai.classify import classify_item
from ai.summarize import summarize_items
from database.db import init_db, save_items
from reports.daily_report import write_daily_report, write_html_report

ROOT = Path(__file__).resolve().parent


def load_config():
    config_path = ROOT / "config.yaml"
    with config_path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main():
    load_dotenv(ROOT / ".env")
    config = load_config()

    db_path = ROOT / config["app"]["database_path"]
    report_path = ROOT / config["app"]["report_path"]
    html_report_path = ROOT / config["app"].get("html_report_path", "docs/index.html")

    init_db(db_path)

    raw_items = collect_rss(
        config["collection"]["rss_feeds"],
        max_items=config["collection"].get("max_items_per_source", 5),
    )
    filtered_items = filter_items(raw_items, config["filter"].get("keywords", []))

    enriched_items = []
    for item in filtered_items:
        item["category"] = classify_item(item)
        enriched_items.append(item)

    save_items(db_path, enriched_items)
    summary_prompt = (ROOT / "prompts" / "summary_prompt.txt").read_text(encoding="utf-8")
    summary = summarize_items(enriched_items, prompt=summary_prompt)
    write_daily_report(report_path, enriched_items, summary)
    write_html_report(html_report_path, enriched_items, summary)

    print(f"Collected {len(raw_items)} items, kept {len(enriched_items)} relevant items.")
    print(f"Markdown report written to: {report_path}")
    print(f"GitHub Pages HTML written to: {html_report_path}")


if __name__ == "__main__":
    main()


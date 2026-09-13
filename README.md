# AI Intelligence Radar v1

A small local project skeleton for collecting AI-related updates, filtering them, saving them to SQLite, and producing a daily Markdown report.

## Quick start

```powershell
cd C:\Users\User\Desktop\AI_Intelligence_Radar_v1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

The first run creates `database/radar.db` and writes a daily report to `reports/latest_daily_report.md`.

## Current status

This is a runnable minimum version. API collectors are placeholders for now; RSS collection already works once dependencies are installed.
## GitHub Pages output

Running `python main.py` now also writes a mobile-friendly web page to `docs/index.html`.

To publish it with GitHub Pages, push this project to GitHub and set Pages to deploy from the `docs` folder on the main branch. Your phone can then open the GitHub Pages URL to view the latest radar report.
## AI summary

Set `OPENAI_API_KEY` in `.env` for local runs. For GitHub Actions, add the same value as a repository secret named `OPENAI_API_KEY`.

The summary prompt is stored in `prompts/summary_prompt.txt` and is configured to produce Traditional Chinese output.

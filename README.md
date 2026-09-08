# fde-roadmap

My 90-day journey from zero to a job-ready Forward Deployed Engineer, tracked day by day.

Started: 2026-09-07

## What's in here
Each day of the roadmap gets its own folder or script as I build:
- Weeks 1-5: full-stack foundations (Python, FastAPI, HTML/CSS/JS, React, cloud deploy)
- Weeks 6-9: data & AI engineering (SQL, ETL pipelines, Claude API, RAG/agents)
- Weeks 10-11: two portfolio capstone projects
- Weeks 12-13: resume, networking, interview prep

## Scripts

### `day6_automation.py`
Fetches a top-20 crypto market snapshot from CoinGecko's free public API,
cleans it with pandas (renames columns, uppercases symbols, fills missing
24h-change values, sorts by market cap), and saves it to
`day6_crypto_snapshot.csv`.

**Run it:**
```bash
python -m venv venv                    # first time only
source venv/Scripts/activate           # Windows Git Bash
pip install requests pandas
python day6_automation.py
```

### `day5_json_shapes.py`
Pulls a GitHub user's public repos, extracts a few fields from the nested
JSON, writes them back out to `day5_repos_summary.json`, and loads the raw
response into a pandas DataFrame with `json_normalize`. Run the same way as
above.

### `day4_api_call.py`
Minimal example of calling a public API with `requests` and handling a
failed request without crashing.

## Log
- **Day 1** — set up dev environment (VS Code, Python, terminal basics)
- **Day 2** — git + GitHub basics, this repo
- **Day 3** — venv basics, package isolation
- **Day 4** — calling APIs with `requests`, graceful error handling
- **Day 5** — nested JSON, writing JSON back out, pandas `json_normalize`
- **Day 6** — first real automation script: API → pandas clean → CSV

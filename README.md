# Atlass E-commerce OSINT Pipeline

> Trend research pipeline that discovers trending data/AI topics via OSINT (GitHub API + Hacker News + Reddit), analyzes them, and generates case studies with source grading.

## 🚀 Quick Start

```bash
git clone https://github.com/ELATLASS/atlass-ecommerce.git
cd atlass-ecommerce
pip install -r requirements.txt
python trend_research.py
```

## 📋 Configuration

Set environment variables for API access:

```bash
export GITHUB_TOKEN=ghp_your_token    # For GitHub API (auth: 5000 req/h vs 60 unauth)
export HN_API_KEY=your_key            # Optional: Hacker News API key
```

Or use a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
# Edit .env with your credentials
```

## 📊 Pipeline Overview

```
trend_research.py
├── search_github_topics()          # GitHub API: trending repos
├── search_hacker_news()            # HN API: top stories
├── search_reddit()                 # Reddit API: subreddit search
├── analyze_trends()                # Aggregate + grade sources
├── generate_case_study()           # Write Markdown case study
├── publish_to_notion()             # Optional: Notion database
└── save_summary()                  # data/trends_summary.json
```

## 📁 Output Structure

```
data/
├── trends.json           # Raw trend data (full)
├── trends_summary.json   # Aggregated metrics (small)

case-studies/
└── YYYY-MM-DD-topic.md   # Generated case study
```

## 🔐 Source Grading

Each data source is graded:
- ✅ **Confirmed** — Direct API response (GitHub, HN API)
- 🔍 **Indice** — Forum/discussion mention (Reddit title/score)
- 🔄 **À vérifier** — Estimated/projection data

## 🧪 Tests

Run the test suite:
```bash
pip install pytest
python -m pytest tests/ -v
```

Tests cover:
- Module imports
- Trend queries non-empty
- JSON output validity
- Requirements.txt completeness

## 📦 Dependencies

See `requirements.txt`:
- `requests` — HTTP client for API calls
- `pandas` — Data analysis
- `ruff` — Linter
- `pytest` — Testing

## ⚙️ CI/CD

- **CI**: Lint + tests auto-run on every PR/Push to `main` or `dev`
- **Release**: Auto-generates tagged releases on push to `main`
- **Deploy**: GitHub Pages deploy on `main` push

## 📝 License

MIT — by [Atlass/Nous Research](https://nousresearch.com)

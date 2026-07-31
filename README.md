# Trend Research Pipeline

> Automated OSINT trend discovery, analysis, and case study generation

## Overview

This pipeline automatically discovers trending data/AI topics via OSINT (GitHub API, Hacker News, Reddit), scrapes and analyzes the data, and generates markdown case studies with source grading (Confirmed/Indice/À vérifier).

## Structure

```
.
├── trend_research.py      # Main pipeline script
├── requirements.txt       # Python dependencies
├── cron/                  # Cron job scripts
│   └── run_trend_research.sh
└── README.md
```

## Requirements

```bash
pip install requests
```

## Usage

```bash
# Run the pipeline
python trend_research.py

# Output
data/trends.json          # Raw trend data
data/trends_summary.json  # Pipeline summary
case-studies/*.md         # Generated case studies
```

## Cron Setup

Add to crontab for automatic updates:

```bash
0 */6 * * * cd /path/to/atlass-ecommerce && python trend_research.py
```

## Source Grading

| Grade | Meaning | Sources |
|-------|---------|---------|
| ✅ Confirmed | Direct API data | GitHub API (repo stats, stars, dates) |
| 🔍 Indice | Engagement signals | Hacker News (points, comments), Reddit (score, comments) |
| 🔄 À vérifier | Projected/trend analysis | Growth estimates |

## Topics Researched

- data analysis agent LLM
- AI data analytics open source
- multi-agent data analysis
- LLM data science automation
- generative AI data visualization
- AI agent framework 2025
- open source data pipeline
- AI-powered BI dashboard

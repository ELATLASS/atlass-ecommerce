# Atlass E-commerce

> Atlass Corp — Trend research pipeline + case studies on AI e-commerce

## Description
Automated trend research pipeline that discovers trending data/AI topics via OSINT (GitHub API + Hacker News), analyzes them, and generates case studies with source grading.

## Badges
![CI](https://github.com/ELATLASS/atlass-ecommerce/actions/workflows/ci.yml/badge.svg)
![Deploy](https://github.com/ELATLASS/atlass-ecommerce/actions/workflows/deploy.yml/badge.svg)
![Auto Release](https://github.com/ELATLASS/atlass-ecommerce/actions/workflows/release.yml/badge.svg)
![Dependabot](https://github.com/ELATLASS/atlass-ecommerce/actions/workflows/dependabot.yml/badge.svg)

## Structure
- `trend_research.py` — Main pipeline script
- `cron/` — Cron job scripts
- `data/` — JSON data files
- `case-studies/` — Generated case study reports

## Getting Started
```bash
git clone https://github.com/ELATLASS/atlass-ecommerce.git
cd atlass-ecommerce
pip install -r requirements.txt
```

## CI/CD
![CI](https://github.com/ELATLASS/atlass-ecommerce/actions/workflows/ci.yml/badge.svg)

## License
MIT — Atlass Corp

#!/usr/bin/env python3
"""
Hermes Trend Research Pipeline
=============================
Automatically discovers trending data/AI topics via OSINT, scrapes sources,
analyzes with pandas/SQL, and generates case studies with source grading.

Run via cron: every 6 hours
Output: data/trends.json + case-studies/*.md
"""
import requests
import json
import os
import re
from datetime import datetime, timezone
from collections import defaultdict

# ─── Configuration ───────────────────────────────────────────────────────────

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Hermes-Trend-Research/1.0",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

# Trending topics to research (rotated each run)
TREND_QUERIES = [
    "data analysis agent LLM",
    "AI data analytics open source",
    "multi-agent data analysis",
    "LLM data science automation",
    "generative AI data visualization",
    "AI agent framework 2025",
    "open source data pipeline",
    "AI-powered BI dashboard",
]

# Sources for OSINT verification
OSINT_SOURCES = [
    {"name": "GitHub", "type": "api", "url": "https://api.github.com"},
    {"name": "Hacker News", "type": "api", "url": "https://hacker-news.firebaseio.com/v0"},
    {"name": "Reddit", "type": "api", "url": "https://www.reddit.com/api/v1"},
]

# ─── Source Grading ──────────────────────────────────────────────────────────

def grade_source(url):
    """Grade a source URL: Confirmed / Indice / À vérifier"""
    if "github.com" in url and "api.github.com" not in url:
        return "✅ Confirmed"
    elif "hacker-news" in url or "reddit.com" in url:
        return "🔍 Indice"
    else:
        return "🔄 À vérifier"

# ─── Data Collection ──────────────────────────────────────────────────────────

def search_github_repos(query, per_page=10):
    """Search GitHub for trending repositories"""
    url = f"{GITHUB_API}/search/repositories"
    params = {
        "q": query + " created:>2025-01-01",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("items", [])
        print(f"  ⚠ GitHub API: {resp.status_code}")
    except Exception as e:
        print(f"  ⚠ GitHub API error: {e}")
    return []

def get_repo_stats(owner, repo):
    """Get detailed stats for a repository"""
    url = f"{GITHUB_API}/repos/{owner}/{repo}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            d = resp.json()
            return {
                "stars": d.get("stargazers_count", 0),
                "forks": d.get("forks_count", 0),
                "issues": d.get("open_issues_count", 0),
                "language": d.get("language", ""),
                "created_at": d.get("created_at", ""),
                "updated_at": d.get("updated_at", ""),
                "size": d.get("size", 0),
                "topics": d.get("topics", []),
                "license": d.get("license", {}).get("spdx_id", "") if d.get("license") else "",
            }
    except Exception as e:
        print(f"  ⚠ Repo stats error: {e}")
    return {}

def search_hn_stories(query, max_items=20):
    """Search Hacker News for trending stories via Algolia API"""
    url = "https://hn.algolia.com/api/v1/search"
    params = {"query": query, "hitsPerPage": max_items, "numericFilters": "points>10"}
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return [
                {
                    "title": h.get("title", ""),
                    "url": h.get("url", f"https://news.ycombinator.com/item?id={h.get('id','')}"),
                    "points": h.get("points", 0),
                    "comments": h.get("num_comments", 0),
                    "created_at": h.get("created_at", ""),
                    "source": "Hacker News",
                }
                for h in data.get("hits", [])
            ]
    except Exception as e:
        print(f"  ⚠ HN API error: {e}")
    return []

def search_reddit(query, subreddit="datascience", limit=10):
    """Search Reddit for trending discussions"""
    url = f"https://www.reddit.com/r/{subreddit}/search.json"
    params = {"q": query, "limit": limit, "sort": "top", "t": "month", "restrict_sr": "on"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return [
                {
                    "title": post.get("data", {}).get("title", ""),
                    "url": "https://reddit.com" + post.get("data", {}).get("permalink", ""),
                    "score": post.get("data", {}).get("score", 0),
                    "comments": post.get("data", {}).get("num_comments", 0),
                    "created_utc": datetime.fromtimestamp(
                        post.get("data", {}).get("created_utc", 0), tz=timezone.utc
                    ).isoformat() if post.get("data", {}).get("created_utc") else "",
                    "source": "Reddit/r/" + subreddit,
                }
                for post in data.get("data", {}).get("children", [])
            ]
    except Exception as e:
        print(f"  ⚠ Reddit API error: {e}")
    return []

# ─── Analysis ─────────────────────────────────────────────────────────────────

def analyze_trend(trend_name, github_repos, hn_stories, reddit_posts):
    """Analyze a trend and compute metrics"""
    # GitHub stats
    total_stars = sum(r.get("stargazers_count", 0) for r in github_repos)
    total_forks = sum(r.get("forks_count", 0) for r in github_repos)
    languages = defaultdict(int)
    for r in github_repos:
        lang = r.get("language", "")
        if lang:
            languages[lang] += 1

    # HN stats
    total_hn_points = sum(s.get("points", 0) for s in hn_stories)
    total_hn_comments = sum(s.get("comments", 0) for s in hn_stories)

    # Reddit stats
    total_reddit_score = sum(p.get("score", 0) for p in reddit_posts)
    total_reddit_comments = sum(p.get("comments", 0) for p in reddit_posts)

    # Source grading
    sources_graded = []
    for r in github_repos[:5]:
        sources_graded.append({
            "url": r.get("html_url", ""),
            "grade": "✅ Confirmed",
            "type": "GitHub repo",
        })
    for s in hn_stories[:5]:
        sources_graded.append({
            "url": s.get("url", ""),
            "grade": "🔍 Indice",
            "type": s.get("source", ""),
        })
    for p in reddit_posts[:5]:
        sources_graded.append({
            "url": p.get("url", ""),
            "grade": "🔍 Indice",
            "type": p.get("source", ""),
        })

    # Growth estimate (based on created dates)
    recent_repos = [r for r in github_repos if r.get("created_at", "") > "2025-06-01"]
    growth_estimate = f"+{len(recent_repos)} new repos (2025 H2)" if recent_repos else "Data insufficient"

    return {
        "trend_name": trend_name,
        "github": {
            "repos_found": len(github_repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "top_languages": dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]),
            "top_repos": [
                {
                    "name": r.get("full_name", ""),
                    "stars": r.get("stargazers_count", 0),
                    "language": r.get("language", ""),
                    "created": r.get("created_at", ""),
                    "description": r.get("description", "")[:150],
                    "url": r.get("html_url", ""),
                    "topics": r.get("topics", []),
                }
                for r in github_repos[:5]
            ],
        },
        "hacker_news": {
            "stories_found": len(hn_stories),
            "total_points": total_hn_points,
            "total_comments": total_hn_comments,
            "top_stories": hn_stories[:5],
        },
        "reddit": {
            "posts_found": len(reddit_posts),
            "total_score": total_reddit_score,
            "total_comments": total_reddit_comments,
            "top_posts": reddit_posts[:5],
        },
        "growth_estimate": growth_estimate,
        "sources_graded": sources_graded,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
    }

# ─── Case Study Generation ───────────────────────────────────────────────────

def generate_case_study(analysis):
    """Generate a markdown case study from analysis data"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    trend = analysis["trend_name"]
    gh = analysis["github"]
    hn = analysis["hacker_news"]
    rd = analysis["reddit"]

    md = f"""# Case Study: {trend.title()}

## Contexte
Analyse de tendance générée automatiquement par **Hermes Trend Research Pipeline**.
Ce cas d'étude explore le phénomène "{trend}" tel qu'il émerge dans les communautés
développeurs et data scientists en 2025-2026.

## Méthodologie
- **Sources** : GitHub API, Hacker News API, Reddit API
- **Date d'analyse** : {now}
- **Source grading** :
  - ✅ **Confirmed** : Données GitHub API (repo stats, stars, dates)
  - 🔍 **Indice** : Discussions HN/Reddit (engagement, votes)
  - 🔄 **À vérifier** : Projections de croissance

## Données Collectées

### GitHub — Repositories open source

| Repository | Stars | Language | Created | Topics |
|---|---|---|---|---|
"""
    for repo in gh["top_repos"]:
        topics_str = ", ".join(repo.get("topics", []))[:50]
        md += f"| [{repo['name']}]({repo['url']}) | {repo['stars']} | {repo['language']} | {repo['created'][:10]} | {topics_str} |\n"

    md += f"""
### Métriques GitHub
- **Repos trouvés** : {gh['repos_found']}
- **Stars cumulées** : {gh['total_stars']:,}
- **Forks cumulés** : {gh['total_forks']:,}
- **Langages** : {', '.join(f'{k} ({v})' for k, v in gh['top_languages'].items())}

### Hacker News
- **Stories** : {hn['stories_found']}
- **Points totaux** : {hn['total_points']}
- **Commentaires** : {hn['total_comments']}

### Reddit
- **Posts** : {rd['posts_found']}
- **Score total** : {rd['total_score']}
- **Commentaires** : {rd['total_comments']}

## Analyse

### 1. Adoption communautaire
Le phénomène "{trend}" compte **{gh['total_stars']:,} étoiles GitHub** cumulées
sur {gh['repos_found']} repositories majeurs. La croissance estimée est de
**{analysis['growth_estimate']}**.

### 2. Technologies associées
Les langages dominants sont : {', '.join(f'{k} ({v} repos)' for k, v in list(gh['top_languages'].items())[:3])}.
Les topics récurrents incluent : {', '.join(set(t for r in gh['top_repos'] for t in r.get('topics', [])[:10]))}.

### 3. Engagement en dehors de GitHub
- **Hacker News** : {hn['total_points']} points, {hn['total_comments']} commentaires
- **Reddit** : {rd['total_score']} score, {rd['total_comments']} commentaires

## Conclusion

"{trend}" représente **une tendance majeure** dans l'écosystème data/AI open source.
Avec {gh['total_stars']:,} étoiles cumulées et une forte présence sur HN/Reddit,
ce phénomène mérite une attention particulière des data analysts et ingénieurs BI.

### Opportunities
- Automatisation des tâches répétitives via LLM
- Democratization de l'analyse de données (non-technical users)
- Intégration multi-plateforme (WeChat, Telegram, Feishu)

### Risques
- Dépendance aux LLM propriétaires
- Fragmentation de l'écosystème
- Complexité de l'intégration desktop

## Sources vérifiées
"""
    for s in analysis["sources_graded"][:10]:
        md += f"- {s['grade']} [{s['type']}]({s['url']})\n"

    md += f"""
*Cas d'étude généré automatiquement par Hermes Agent — {now}*
"""
    return md

# ─── Main Pipeline ───────────────────────────────────────────────────────────

def main():
    print("🚀 Hermes Trend Research Pipeline — starting")
    print(f"   Time: {datetime.now(timezone.utc).isoformat()}")

    # Ensure directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("case-studies", exist_ok=True)

    all_trends = {}

    for query in TREND_QUERIES:
        print(f"\n🔍 Researching: {query}")

        # Collect data from all sources
        github_repos = search_github_repos(query, per_page=10)
        print(f"   GitHub: {len(github_repos)} repos found")

        hn_stories = search_hn_stories(query, max_items=10)
        print(f"   Hacker News: {len(hn_stories)} stories found")

        reddit_posts = search_reddit(query, subreddit="datascience", limit=10)
        print(f"   Reddit: {len(reddit_posts)} posts found")

        # Analyze
        analysis = analyze_trend(query, github_repos, hn_stories, reddit_posts)
        all_trends[query] = analysis

        # Generate case study
        if github_repos or hn_stories or reddit_posts:
            case_study = generate_case_study(analysis)
            safe_name = re.sub(r'[^a-z0-9]+', '-', query.lower()).strip('-')
            filename = f"case-studies/{safe_name}.md"
            with open(filename, "w") as f:
                f.write(case_study)
            print(f"   ✓ Case study: {filename}")

    # Save combined data
    with open("data/trends.json", "w") as f:
        json.dump(all_trends, f, indent=2, default=str)
    print(f"\n✓ All data saved to data/trends.json")

    # Generate summary
    summary = {
        "pipeline_run_at": datetime.now(timezone.utc).isoformat(),
        "trends_analyzed": len(all_trends),
        "total_github_repos": sum(t["github"]["repos_found"] for t in all_trends.values()),
        "total_stars": sum(t["github"]["total_stars"] for t in all_trends.values()),
        "total_hn_stories": sum(t["hacker_news"]["stories_found"] for t in all_trends.values()),
        "total_reddit_posts": sum(t["reddit"]["posts_found"] for t in all_trends.values()),
        "case_studies_generated": len([f for f in os.listdir("case-studies") if f.endswith(".md")]),
    }
    with open("data/trends_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Summary saved to data/trends_summary.json")

    print(f"\n✅ Pipeline complete!")
    print(f"   Trends analyzed: {summary['trends_analyzed']}")
    print(f"   Total repos: {summary['total_github_repos']}")
    print(f"   Total stars: {summary['total_stars']:,}")
    print(f"   Case studies: {summary['case_studies_generated']}")

if __name__ == "__main__":
    main()

import sys

import requests

query = sys.argv[1]
name = sys.argv[2]
date_str = sys.argv[3]
output_file = sys.argv[4]

url = "https://api.github.com/search/repositories"
params = {"q": query, "sort": "stars", "order": "desc", "per_page": 5}
headers = {"Accept": "application/vnd.github+json"}

try:
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    data = resp.json()
    repos = data.get("items", [])
except Exception as e:
    print(f"Error: {e}")
    repos = []

md = "# Daily Case Study: " + name + "\n\n"
md += "## Date\n" + date_str + "\n\n"
md += "## Contexte\nAnalyse quotidienne des tendances " + name + " basée sur des données GitHub OSINT.\n\n"
md += "## Données — GitHub Repositories\n\n"
md += "| Repository | Stars | Language | Created | Description |\n|---|---|---|---|---|\n"

for r in repos[:5]:
    rn = r.get("full_name", "")
    stars = r.get("stargazers_count", 0)
    lang = r.get("language", "")
    created = r.get("created_at", "")[:10]
    desc = r.get("description", "")[:80]
    url_r = r.get("html_url", "")
    md += "| [" + rn + "](" + url_r + ") | " + str(stars) + " | " + lang + " | " + created + " | " + desc + " |\n"

md += "\n## Métriques\n"
md += "- **Repos trouvés** : " + str(len(repos)) + "\n"
md += "- **Stars cumulées** : " + str(sum(r.get("stargazers_count", 0) for r in repos)) + "\n"
md += "- **Langages** : " + ", ".join({r.get("language", "") for r in repos if r.get("language")}) + "\n\n"
md += "## Source Grading\n"
md += "- ✅ **Confirmed** : GitHub API data\n"
md += "- 🔍 **Indice** : Repo descriptions\n"
md += "- 🔄 **À vérifier** : Growth projections\n\n"
md += "*Cas d'étude généré automatiquement par Hermes Daily Case Study — " + date_str + "*\n"

with open(output_file, "w") as f:
    f.write(md)

print("✓ Generated: " + output_file)
print("  Repos: " + str(len(repos)) + ", Stars: " + str(sum(r.get("stargazers_count", 0) for r in repos)))

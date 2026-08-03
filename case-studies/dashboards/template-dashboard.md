# Market Analysis Dashboard Template

> Auto-generated dashboard template for trend research results.
> Place in `case-studies/dashboards/` and customize per-topic.

## 📊 Trend Metrics — {{topic}}

Generated: {{date}}

### Overview Table

| Metric | Value | Change |
|---|---|---|
| GitHub Repos Found | {{repos_found}} | {{repos_growth}} |
| Total Stars | {{total_stars}} | {{stars_growth}} |
| Hacker News Stories | {{hn_stories}} | {{hn_growth}} |
| Reddit Posts | {{reddit_posts}} | {{reddit_growth}} |

### Language Distribution

| Language | Count | % Share |
|---|---|---|
{% for lang, count in languages.items() %}
| {{lang}} | {{count}} | {{ "%.1f"|format(count / total_repos * 100) }}% |
{% endfor %}

### Top Repositories

| Repo | Stars | Language | Created | Description |
|---|---|---|---|---|
{% for repo in top_repos %}
| [{{repo.name}}]({{repo.url}}) | {{repo.stars}} | {{repo.language}} | {{repo.created[:10]}} | {{repo.description[:80]}} |
{% endfor %}

### Trend Analysis

#### Growth Trajectory
```mermaid
graph LR
    A[Week -3] --> B[Week -2]
    B --> C[Week -1]
    C --> D[Current Week]
    A -->|{{week_3_count}} repos| B
    B -->|{{week_2_count}} repos| C
    C -->|{{week_1_count}} repos| D
```

#### Source Grading Breakdown
- ✅ Confirmed: {{confirmed_count}} sources (API responses)
- 🔍 Indice: {{indice_count}} sources (forum mentions)
- 🔄 À vérifier: {{unverified_count}} sources (estimates)

### Recommendations

{% if growth_rate > 20 %}
- **High growth detected** (+{{growth_rate}}%). Consider deep dive analysis.
- Recommend generating a full case study with `{{repo_name}}` as lead example.
{% elif growth_rate > 5 %}
- **Moderate growth** (+{{growth_rate}}%). Monitor for next cycle.
- Consider adding to weekly alert filter.
{% else %}
- **Stable/flat trend**. No immediate action needed.
- Archive source for historical comparison.
{% endif %}

### Next Steps

1. [ ] Verify top {{repo_name}} repo for detailed analysis
2. [ ] Cross-reference with {{hn_stories}} HN stories
3. [ ] Generate case study: `python generate_cs.py "{{topic}}"`

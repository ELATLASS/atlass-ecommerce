"""Minimal test suite for atlass-ecommerce trend research pipeline."""
import json
import os
import sys

# Add repo root to path so we can import trend_research
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _REPO_ROOT)


def test_trend_research_imports():
    """Ensure trend_research.py can be imported without runtime errors."""
    import trend_research
    assert hasattr(trend_research, "GITHUB_API")
    assert hasattr(trend_research, "TREND_QUERIES")


def test_trend_queries_non_empty():
    """Trend queries must be defined and non-empty."""
    from trend_research import TREND_QUERIES
    assert len(TREND_QUERIES) > 0


def test_data_trends_json_valid():
    """If data/trends.json exists, it must be valid JSON."""
    data_path = os.path.join(_REPO_ROOT, "data", "trends.json")
    if os.path.exists(data_path):
        with open(data_path) as f:
            data = json.load(f)
        assert isinstance(data, (dict, list))


def test_requirements_has_required_deps():
    """requirements.txt must list requests, pandas, and ruff."""
    req_path = os.path.join(_REPO_ROOT, "requirements.txt")
    assert os.path.exists(req_path), f"requirements.txt not found at {req_path}"
    with open(req_path) as f:
        content = f.read()
    for dep in ["requests", "pandas", "ruff"]:
        assert dep in content, f"'{dep}' missing from requirements.txt"

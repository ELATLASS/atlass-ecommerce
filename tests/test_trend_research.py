"""Minimal test suite for atlass-ecommerce trend research pipeline."""
import json
import os
import sys

import pytest


def test_trend_research_imports():
    """Ensure trend_research.py can be imported without runtime errors."""
    sys.path.insert(0, os.path.dirname(__file__))
    import trend_research
    assert hasattr(trend_research, "GITHUB_API")
    assert hasattr(trend_research, "TREND_QUERIES")


def test_trend_queries_non_empty():
    """Trend queries must be defined and non-empty."""
    sys.path.insert(0, os.path.dirname(__file__))
    from trend_research import TREND_QUERIES
    assert len(TREND_QUERIES) > 0


def test_data_trends_json_valid():
    """If data/trends.json exists, it must be valid JSON."""
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", "trends.json"
    )
    data_path = os.path.abspath(data_path)
    if os.path.exists(data_path):
        with open(data_path) as f:
            data = json.load(f)
        assert isinstance(data, (dict, list))


def test_requirements_has_requests():
    """requirements.txt must list requests."""
    req_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "requirements.txt"
    )
    req_path = os.path.abspath(req_path)
    with open(req_path) as f:
        content = f.read()
    assert "requests" in content

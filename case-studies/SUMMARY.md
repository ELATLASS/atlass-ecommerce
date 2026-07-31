# Case Studies — Atlass Corp

This directory contains auto-generated case studies from the Hermes Trend Research Pipeline.

## Available Studies

1. [LLM Data Agents (2025-2026)](llm-data-agents-2025-2026.md) — Analysis of the explosion of LLM-powered data analysis agents
2. [Generative AI E-Commerce (2025-2026)](generative-ai-ecommerce-2025-2026.md) — How generative AI is transforming e-commerce

## Pipeline

Case studies are generated every 6 hours by the Hermes cron job:
- Collects data from GitHub API + Hacker News API
- Analyzes trends with source grading (Confirmed/Indice/À vérifier)
- Generates markdown reports with metrics and recommendations

## Next Run

The portfolio monitor cron job runs every 6 hours.

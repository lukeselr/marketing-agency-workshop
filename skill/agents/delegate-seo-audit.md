---
name: delegate-seo-audit
description: One-time SEO audit + monthly re-check. Pulls technical, page-level, and content gaps. Feeds Phase 11 organic calendar.
---

## When to invoke
First run during Phase 1, then monthly after Phase 12.

## Context
- Domain from baseline
- Industry classification

## Delegation
1. `claude-seo/skills/seo-audit` (full)
2. `claude-seo/skills/seo-page` (top 10 pages)
3. `claude-seo/skills/seo-technical` (Core Web Vitals + crawl)
4. `claude-seo/skills/seo-content` (keyword gaps vs competitors)

## Read back
`.state/seo-audit.md` with prioritised fixes by impact / effort.

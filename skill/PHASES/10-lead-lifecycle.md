# Phase 10 — Lead lifecycle automation

Every lead gets agency-grade response time + nurture without owner action.

## How it runs

```bash
bash ~/.claude/skills/marketing-agency/scripts/lead-lifecycle-deploy.py
```

## What it does

1. Detects industry from `.state/business-baseline.md`
2. Picks the matching template from `templates/lifecycle-sequences/` (12 industries: default, trades, real-estate, hospitality, health, ecom, saas, coaching, legal, marketing-agency, b2b-services, b2c-local)
3. Writes a deploy plan to `.state/lifecycle/deploy-plan.json`
4. Hands off to `delegate-email-drip` + `delegate-sms-instant` agents which generate voice-graded copy and push to GHL / ManyChat as DRAFT

## Components

- **Instant reply**: SMS within 60 sec, email within 90 sec
- **6-step drip**: day 0 / 1 / 3 / 7 / 14 / 30
- **No-show recovery**: 3hr + 24hr
- **Lead scoring**: form + pageviews + UTM + manual signals → 0-10 score
- **Hot-lead handoff**: Slack ping with LinkedIn snapshot when score ≥ 8

## Owner approval gate

All drafts land in GHL/ManyChat as DRAFT. Owner reviews in `~/marketing/calendar/draft-posts/lifecycle/` and approves activation explicitly. Never auto-publish.

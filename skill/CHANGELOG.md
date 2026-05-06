# Changelog

## v2.1.1 (2026-05-07) — workshop public release
- Sanitize for public attendee repo distribution
- External-skill resolver now keyed on optional `MA_EXTERNAL_KIT_REPO` env var, not a hard-coded private repo
- Update.sh now points at `lukeselr/marketing-agency-workshop` (override via `MA_REPO`)
- Embed firewall rules inline in `shared/voice-grade-config.json` so the skill is portable

## v2.1.0 (2026-05-06) — audit-driven hardening

Tier S fixes from the 20-agent stochastic consensus audit.

**Security**
- Stop leaking live tokens to stdout. All 6 Playwright specs (Meta x2, Google Ads x2, LinkedIn x2) now write directly to `~/.marketing-agency/tokens/<platform>.json` mode 600. stdout receives only `{ok, wrote: <key>}` confirmation.
- Sanitize `discover.sh` shell injection. `bash -c "$cmd"` removed; scrapers invoked as direct argv. INPUT validated against shell metacharacters.

**Truth**
- Add 3 missing agent docs (`connector-recommender`, `weekly-report-orchestrator`, `monthly-strategy-orchestrator`).
- Add `PHASES/-1-self-install.md`.
- Add `scripts/poll-approvals.sh` (real implementation, Gmail-MCP polling, idempotent).

**Industry coverage**
- Rewrite all 12 lifecycle templates with genuinely industry-specific instant-SMS, instant-email, 6-step drip, no-show recovery cadence, lead-scoring weights, hot-handoff signal, AU SPAM Act footer + opt-out, ABN line.
- Add 7 new ICP templates: cafe, gym, salon, dentist, mortgage-broker, financial-planner, buyers-agent. 19 total.
- Improve `lead-lifecycle-deploy.py` industry detector (highest-specificity-first ordered rules, 18 industry keywords).

**Attendee path**
- Add `scripts/resolve-external-skills.sh`. Walks every `references/external/*` symlink, repoints to attendee-fallback path, optionally `gh repo clone $MA_EXTERNAL_KIT_REPO` when the env var is set + `gh` is auth-ed. Records misses in `.state/missing-external.json`.
- Add `shared/external_skills.py` helper. `is_available()`, `skip_note()`, `require()` so delegate-* scripts can graceful-skip with plain-English owner-facing notes.
- Wire resolve-external-skills.sh into `install.sh` between pre-flight and dashboard build.

## v2.0.0 (2026-05-06) — elite-agency upgrade
- 39 external skill symlinks, 10 delegate agents, MAP.md routing, 11 MCP connectors (auto-OAuth)
- 4 new phases (9.5 weekly report / 10 lead lifecycle / 11 organic calendar / 12 monthly strategy)
- Phase 6.5 landing CRO + Phase 8 audience-ops upgrade
- /marketing-agency slash command, ~/marketing/ owner dashboard
- 12 industry lifecycle templates, state-aware run.sh

## v1.0.0 (2026-05-05) — first ship
- 14 free scrapers, 20 Playwright specs across 3 platforms
- 10 phase docs, agents/templates/references
- Installers (Mac+Windows), package-zip with secrets check

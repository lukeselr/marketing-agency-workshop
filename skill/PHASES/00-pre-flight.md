# Phase 0 — Pre-flight

Run by `scripts/check-preflight.sh`. Silent for the user unless something is missing.

## Checks

| Check | Required | Auto-install? |
|---|---|---|
| Node 18+ | yes | offer brew/nvm/winget |
| Python 3.10+ | yes | offer brew |
| jq | yes | offer brew/apt |
| curl | yes | usually present |
| Playwright MCP | yes | install via Claude Code marketplace |
| gh CLI | yes (Sprint 4 distribution) | offer brew |

## Cost transparency

Before continuing, the user sees `shared/cost-transparency.md`.

## Selectors drift check

Runs `shared/selectors-version-check.sh`. Warns if any platform's `selectors.json` is older than 30 days.

## State init

Creates `~/.marketing-agency/tokens/` (mode 700) and `.state/` directories. Writes `.state/preflight.json` with all check results.

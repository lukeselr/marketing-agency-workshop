# Phase -1 — Self-install

Mirrors the `xero-mcp-setup` Phase -1 pattern: before Phase 0 pre-flight runs, the skill makes sure its own runtime is in place and any external skills it depends on are reachable.

This phase fires automatically the first time `bash install.sh` (or `/marketing-agency`) runs on a machine. Subsequent runs detect the green-state file and skip.

## What runs

1. **Toolchain check** — Node 18+, Python 3.10+, git, jq, curl. If missing on macOS, attempt `brew install` (no-sudo). On Linux/WSL, attempt `apt-get install -y` if `sudo -n` is allowed; otherwise print exact commands and exit non-zero.
2. **Python deps** — `pip3 install --user --quiet requests beautifulsoup4 markdown jinja2`.
3. **Playwright browsers** — `npx -y playwright install chromium` (cached after first run).
4. **Runtime dirs** — `~/.marketing-agency/{tokens,cache,logs}` mode 700.
5. **External skill resolution** — for every entry in `references/external/`:
   - If the symlink target exists, leave it.
   - Otherwise, if `MA_EXTERNAL_KIT_REPO` is set (e.g. `org/private-skill-bundle`) and `gh` is auth-ed, shallow-clone that repo into `~/.marketing-agency/external/` and re-point the symlink.
   - If clone fails (no auth, no network), record the missing skill in `.state/missing-external.json` and the orchestrator will graceful-skip those delegations with a plain-English note to the owner.
6. **MCP wiring** — chain `scripts/install-mcp/connect-all.sh` (idempotent — skips already-green connectors).
7. **State checkpoint** — write `.state/self-install.json`:
   ```json
   { "version": "2.1.0", "completed_at": "<iso>", "skipped": [], "warnings": [] }
   ```

## Failure modes

- **Toolchain blocker** — print "Install <tool>, then re-run", exit 2. Never auto-sudo.
- **Network blocker** — record offline, skip optional steps, continue. Phase 0 pre-flight will surface remaining gaps.
- **Token mode > 600** — auto-chmod, log warning.
- **Disk space < 1GB free in HOME** — abort with friendly message.

## Verification

```bash
bash ~/.claude/skills/marketing-agency/install.sh --verify-only
# expect: jq, node, python3, playwright chromium, ~/.marketing-agency exists, mode 700, .state/self-install.json present
```

## Why this phase

Without it, attendees on fresh Macs hit cryptic "command not found" errors halfway through Phase 1 and disengage. The xero-mcp-setup pattern proved that a 90-second self-install is worth the build cost — the user opens Terminal, runs one line, and is genuinely ready.

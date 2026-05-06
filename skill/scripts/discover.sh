#!/usr/bin/env bash
# Phase 1 entry — kicks off the parallel auto-discovery pipeline.
# Usage: discover.sh <business_url_or_name>
#
# Runs 14 free scrapers in parallel with per-scraper timeout, streams progress,
# synthesises business-baseline.md.

set -u

INPUT="${1:-}"
if [ -z "$INPUT" ]; then
  echo "Usage: discover.sh <business_url_or_name>"
  exit 1
fi

# Reject inputs containing shell metacharacters that have no business in a URL/name.
# Allow: letters, digits, spaces, dot, dash, underscore, slash, colon, ampersand, plus, comma, apostrophe, percent, query/fragment chars.
if printf '%s' "$INPUT" | LC_ALL=C grep -q '[`$;|<>(){}\\]'; then
  echo "Error: input contains shell metacharacters. Pass a clean URL or business name." >&2
  echo "Got: $INPUT" >&2
  exit 2
fi

if [ ${#INPUT} -gt 500 ]; then
  echo "Error: input >500 chars. Pass a single URL or business name." >&2
  exit 2
fi

SKILL_DIR="$HOME/.claude/skills/marketing-agency"
STATE_DIR="$SKILL_DIR/.state"
SCRAPE_DIR="$STATE_DIR/scrape"
mkdir -p "$SCRAPE_DIR"

# Wipe previous run
rm -f "$SCRAPE_DIR"/*.json 2>/dev/null || true

START=$(date +%s)
LOG="$STATE_DIR/discover.log"
: > "$LOG"

# Per-scraper timeout in seconds (default 60, override via MA_SCRAPER_TIMEOUT)
TO="${MA_SCRAPER_TIMEOUT:-60}"

stream() {
  local elapsed=$(($(date +%s) - START))
  local mins=$((elapsed / 60))
  local secs=$((elapsed % 60))
  local prefix
  prefix=$(printf "[%dm%02ds]" "$mins" "$secs")
  echo "$prefix $*" | tee -a "$LOG"
}

# Cross-platform timeout: prefer GNU coreutils 'timeout', fall back to Perl alarm.
# Executes argv directly (no shell-string eval) so untrusted input cannot inject.
run_with_timeout() {
  local seconds="$1"
  shift
  if command -v timeout > /dev/null 2>&1; then
    timeout "$seconds" "$@"
  elif command -v gtimeout > /dev/null 2>&1; then
    gtimeout "$seconds" "$@"
  else
    perl -e '
      my $sec = shift;
      eval {
        local $SIG{ALRM} = sub { die "timeout\n" };
        alarm $sec;
        my $rc = system(@ARGV);
        alarm 0;
        exit ($rc >> 8);
      };
      if ($@ eq "timeout\n") { exit 124; }
    ' "$seconds" "$@"
  fi
}

# Direct argv execution — no `bash -c` and no eval. INPUT is a positional arg
# to python3, so single quotes / shell metacharacters cannot inject.
run_scraper() {
  local name="$1"; shift
  local output="$SCRAPE_DIR/$name.json"
  (
    if run_with_timeout "$TO" "$@" > "$output" 2>>"$LOG"; then
      local size
      size=$(wc -c < "$output" 2>/dev/null | tr -d ' ' || echo 0)
      stream "$name -- ok (${size} bytes)"
    else
      local rc=$?
      if [ "$rc" -eq 124 ]; then
        stream "$name -- TIMEOUT after ${TO}s"
        printf '{"status":"timeout","scraper":"%s"}\n' "$name" > "$output"
      else
        stream "$name -- skipped or partial (rc=$rc)"
        printf '{"status":"skipped","scraper":"%s"}\n' "$name" > "$output"
      fi
    fi
  ) &
}

echo "$INPUT" > "$STATE_DIR/input.txt"
stream "Starting auto-discovery for: $INPUT"
stream "Spawning 14 parallel scrapers (per-scraper timeout=${TO}s)..."

PY="python3"
SC="$SKILL_DIR/scripts/scrape"

# Site-level
run_scraper "website"    "$PY" "$SC/website.py"     "$INPUT"
run_scraper "dns-host"   "$PY" "$SC/dns-host.py"    "$INPUT"

# Public registries (AU)
run_scraper "abn-lookup" "$PY" "$SC/abn-lookup.py"  "$INPUT"

# Search + maps + listings
run_scraper "google-search"   "$PY" "$SC/google-search.py"        "$INPUT"
run_scraper "google-maps"     "$PY" "$SC/google-maps.py"          "$INPUT"
run_scraper "industry-dirs"   "$PY" "$SC/industry-directories.py" "$INPUT"
run_scraper "reviews"         "$PY" "$SC/reviews.py"              "$INPUT"
run_scraper "news-mentions"   "$PY" "$SC/news-mentions.py"        "$INPUT"

# Social
run_scraper "linkedin-page"     "$PY" "$SC/linkedin-page.py"     "$INPUT"
run_scraper "instagram-public"  "$PY" "$SC/instagram-public.py"  "$INPUT"
run_scraper "facebook-page"     "$PY" "$SC/facebook-page.py"     "$INPUT"

# Ad libraries (FREE + public)
run_scraper "meta-ad-library"        "$PY" "$SC/meta-ad-library.py"        "$INPUT"
run_scraper "linkedin-ad-library"    "$PY" "$SC/linkedin-ad-library.py"    "$INPUT"
run_scraper "google-ads-transparency" "$PY" "$SC/google-ads-transparency.py" "$INPUT"

# Owned (consented)
run_scraper "cloud-drives" "$PY" "$SC/cloud-drives.py" "$INPUT"

stream "All scrapers spawned. Waiting for completion..."
wait

stream "All scrapers complete. Synthesising profile..."
python3 "$SKILL_DIR/scripts/synthesize.py" "$SCRAPE_DIR" "$INPUT" > "$STATE_DIR/business-baseline.md"

ELAPSED=$(($(date +%s) - START))
stream "Done. Total time: ${ELAPSED}s. Profile at $STATE_DIR/business-baseline.md"
echo
echo "Next:"
echo "  cat $STATE_DIR/business-baseline.md   # review"
echo "  bash $SKILL_DIR/scripts/ask-questions.sh   # answer 5 lean questions"

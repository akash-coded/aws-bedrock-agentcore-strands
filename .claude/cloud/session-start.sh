#!/bin/bash
# Run once at the start of a Claude Code cloud session:   bash .claude/cloud/session-start.sh
# Outside a cloud session it does nothing. Safe to run again (after the session's machine was rebuilt, the
# links are gone and this puts them back).
#
# In a cloud session it:
#   - links the owner's skills that have a public source into .claude/skills/, from the copies setup.sh
#     fetches at pinned commits (fetching them first if it has not), so they load as on the owner's machine.
#     Skills on the owner's claude.ai account load in cloud sessions by themselves.
#   - writes the headless Chrome path to $CLAUDE_ENV_FILE when that file exists
#   - prints what the session has and what it must read first
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

input=""
[ -t 0 ] || input="$(timeout 2 cat 2>/dev/null || true)"
source="$(printf '%s' "$input" | python3 -c 'import json, sys
try: print(json.load(sys.stdin).get("source", ""))
except Exception: print("")' 2>/dev/null)"
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
HANDOFF="handoff/round-8/HANDOFF.md"

if [ "$source" = "compact" ]; then
  echo "The context was just compacted. Before going on, re-read sections 4 to 6 of $HANDOFF (the owner's standing rules, the plan, what is still to do) and check your task list against them."
  exit 0
fi

# Folder name in .claude/skills, then its path inside the fetched sources (pinned in setup.sh).
LINKS=(
  "humanizer humanizer"
  "no-ai-slop-skill no-ai-slop/skills/no-ai-slop"
  "taste taste-skill/skills/taste-skill-v1"
  "taste-skill taste-skill/skills/taste-skill"
  "brandkit taste-skill/skills/brandkit"
  "brutalist-skill taste-skill/skills/brutalist-skill"
  "gpt-tasteskill taste-skill/skills/gpt-tasteskill"
  "image-to-code-skill taste-skill/skills/image-to-code-skill"
  "imagegen-frontend-mobile taste-skill/skills/imagegen-frontend-mobile"
  "imagegen-frontend-web taste-skill/skills/imagegen-frontend-web"
  "minimalist-skill taste-skill/skills/minimalist-skill"
  "output-skill taste-skill/skills/output-skill"
  "redesign-skill taste-skill/skills/redesign-skill"
  "soft-skill taste-skill/skills/soft-skill"
  "stitch-skill taste-skill/skills/stitch-skill"
  "transitions-dev transitions.dev/skills/transitions-dev"
  "transitions-polish transitions.dev/skills/transitions-polish"
  "ui-ux-pro-max ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max"
  "banner-design ui-ux-pro-max-skill/.claude/skills/banner-design"
  "brand ui-ux-pro-max-skill/.claude/skills/brand"
  "design ui-ux-pro-max-skill/.claude/skills/design"
  "design-system ui-ux-pro-max-skill/.claude/skills/design-system"
  "slides ui-ux-pro-max-skill/.claude/skills/slides"
  "ui-styling ui-ux-pro-max-skill/.claude/skills/ui-styling"
  "karpathy-guidelines andrej-karpathy-skills/skills/karpathy-guidelines"
  "caveman caveman/skills/caveman"
  "ian-xiaohei-illustrations ian-xiaohei-illustrations-en/ian-xiaohei-illustrations"
)

find_src() {
  for d in ${SKILLS_HOME:-} /opt/claude-skills "$HOME/.cache/claude-skills"; do
    [ -f "$d/ui-ux-pro-max-skill/.pinned" ] && { echo "$d"; return; }
  done
}
SRC="$(find_src)"
if [ -z "$SRC" ]; then
  bash "$ROOT/.claude/cloud/setup.sh" --skills-only >/dev/null 2>&1
  SRC="$(find_src)"
  [ -z "$SRC" ] && for d in /opt/claude-skills "$HOME/.cache/claude-skills"; do [ -d "$d" ] && SRC="$d" && break; done
fi

linked=(); missing=()
mkdir -p "$ROOT/.claude/skills"
for pair in "${LINKS[@]}"; do
  name="${pair%% *}"; rel="${pair#* }"
  dest="$ROOT/.claude/skills/$name"
  # A skill committed to the repository under the same name wins; leave it alone.
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then continue; fi
  target="${SRC:-/nonexistent}/$rel"
  if [ -f "$target/SKILL.md" ]; then
    ln -sfn "$target" "$dest" && linked+=("$name")
  else
    missing+=("$name")
  fi
done

chrome=""
for c in "${CHROME:-}" /usr/local/bin/google-chrome "$(command -v google-chrome 2>/dev/null)" "$(command -v chromium 2>/dev/null)"; do
  if [ -n "$c" ] && [ -x "$c" ]; then chrome="$c"; break; fi
done
if [ -n "$chrome" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export CHROME=\"$chrome\"" >> "$CLAUDE_ENV_FILE"
fi

committed="$(cd "$ROOT/.claude/skills" 2>/dev/null && for d in */; do d="${d%/}"; [ -L "$d" ] || printf '%s ' "$d"; done)"

echo "Cloud session setup (.claude/cloud/session-start.sh):"
if [ -n "$chrome" ]; then
  echo "- Headless Chrome for the site's check tools: $chrome (\$CHROME points at it)."
else
  echo "- Headless Chrome is NOT installed, and the site's check tools need it. Run: bash .claude/cloud/setup.sh (about three minutes). Then set CHROME=/usr/local/bin/google-chrome."
fi
if command -v playwright >/dev/null 2>&1; then
  echo "- Playwright with WebKit is installed, for checks in Safari's engine (module: $(npm root -g 2>/dev/null)/playwright)."
fi
echo "- Skills linked into .claude/skills: ${#linked[@]}. Committed there: ${committed:-none}."
if [ "${#missing[@]}" -gt 0 ]; then
  echo "- Skills that could not be fetched: ${missing[*]}. See .claude/cloud/README.md, section Skills."
fi
echo "- If a skill named above is missing from your skill list, run /reload-skills."
echo "- AWS skills and AWS documentation come from the AWS MCP connector when the owner has enabled it for this session; there are no AWS credentials here."
echo "- Before any work, read $HANDOFF in full: what the move to the cloud did not carry, where the stopped helpers left off, the owner's standing rules, the plan and how to check work before reporting it."
exit 0

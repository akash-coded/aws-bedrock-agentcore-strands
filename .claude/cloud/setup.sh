#!/bin/bash
# Setup for Claude Code cloud sessions on this repository (Ubuntu 24.04, x86_64).
#
# Two ways to use it:
#   1. Paste this whole file into the cloud environment's "Setup script" box (claude.ai/code, the cloud
#      icon above the message box, the environment's settings). It then runs as root before Claude starts,
#      and the result is cached for later sessions when it finishes in under about five minutes.
#   2. Inside a session that is already running:   bash .claude/cloud/setup.sh
#      (or `bash .claude/cloud/setup.sh --skills-only` to fetch only the skills; session-start.sh does that).
#
# What it installs, each step on its own so one failure never blocks the others:
#   - headless Chrome (Chrome for Testing) with its libraries and fonts, behind /usr/local/bin/google-chrome,
#     which the site's check tools use through $CHROME (site/tools/*.mjs, handoff/round-8/tools/*.mjs)
#   - AWS CLI v2 (no credentials: none are stored in a cloud environment, see .claude/cloud/README.md)
#   - the owner's third-party skills at pinned commits; .claude/cloud/session-start.sh links them into
#     .claude/skills/ when a session starts
#   - Playwright with WebKit for checks in Safari's engine, only when the network allows its download host
#
# It always exits 0: a failed optional step is reported, never fatal.

set -u
if [ "$(uname -s)" != "Linux" ]; then
  echo "[setup] This script is for the cloud session's Linux machine; nothing to do on $(uname -s)."
  exit 0
fi
SKILLS_ONLY=0
[ "${1:-}" = "--skills-only" ] && SKILLS_ONLY=1

if [ "$(id -u)" = "0" ]; then SUDO=""; elif command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO="none"; fi
if [ -n "${SKILLS_HOME:-}" ]; then
  :
elif [ "$SUDO" = "none" ]; then
  SKILLS_HOME="${HOME}/.cache/claude-skills"
else
  SKILLS_HOME="/opt/claude-skills"
fi
LOG="${TMPDIR:-/tmp}/skyways-setup.log"
: > "$LOG"
say() { echo "[setup] $*" | tee -a "$LOG"; }
as_root() { if [ "$SUDO" = "none" ]; then return 1; else $SUDO "$@"; fi; }

# ---------------------------------------------------------------------------------------------
# Skills: owner, repository, pinned commit. The folder names the session links are in session-start.sh.
SKILL_REPOS=(
  "humanizer blader/humanizer 9862685f575c65a8247f90369951df1b3416e3d6"
  "no-ai-slop petergyang/no-ai-slop 000650b156983f5159695b441477f4e63b25dc85"
  "taste-skill leonxlnx/taste-skill c184364c58658b2f131b4ae8bd3d206cabb3deee"
  "transitions.dev Jakubantalik/transitions.dev e2d5551656e4d3274e075d1cbd9a95af50f53225"
  "ui-ux-pro-max-skill nextlevelbuilder/ui-ux-pro-max-skill dcc40ff5133ef78276117db0cc34e7b83cc8aeba"
  "andrej-karpathy-skills forrestchang/andrej-karpathy-skills 2c606141936f1eeef17fa3043a72095b4765b9c2"
  "caveman JuliusBrussee/caveman b39c90862855ad2f0813ce775b8bf07a9d6d2a50"
  "ian-xiaohei-illustrations-en tojileon/ian-xiaohei-illustrations-en 18280fc475fbda00efc0da6608860d69028deb6a"
)

fetch_skill_repo() {
  local key="$1" repo="$2" sha="$3" dest="$SKILLS_HOME/$1"
  if [ -f "$dest/.pinned" ] && [ "$(cat "$dest/.pinned")" = "$sha" ]; then return 0; fi
  rm -rf "$dest.tmp" && mkdir -p "$dest.tmp"
  # 1) the archive from codeload.github.com (in the default Trusted list)
  if curl -fsSL --retry 2 --max-time 180 "https://codeload.github.com/$repo/tar.gz/$sha" \
       | tar -xz --strip-components=1 -C "$dest.tmp" 2>>"$LOG"; then
    :
  else
    # 2) git, fetching only that commit
    rm -rf "$dest.tmp" && mkdir -p "$dest.tmp"
    if ! ( cd "$dest.tmp" && git init -q && git remote add origin "https://github.com/$repo.git" \
           && git fetch -q --depth 1 origin "$sha" && git -c advice.detachedHead=false checkout -q FETCH_HEAD \
           && rm -rf .git ) >>"$LOG" 2>&1; then
      rm -rf "$dest.tmp"; say "skills: could not fetch $repo@${sha:0:7}"; return 1
    fi
  fi
  rm -rf "$dest" && mv "$dest.tmp" "$dest" && echo "$sha" > "$dest/.pinned"
  say "skills: $repo@${sha:0:7} ready"
}

fetch_skills() {
  mkdir -p "$SKILLS_HOME" 2>/dev/null || as_root mkdir -p "$SKILLS_HOME"
  [ -w "$SKILLS_HOME" ] || as_root chmod 777 "$SKILLS_HOME" 2>/dev/null || true
  local pids=() line
  for line in "${SKILL_REPOS[@]}"; do
    # shellcheck disable=SC2086
    fetch_skill_repo $line & pids+=($!)
  done
  for p in "${pids[@]}"; do wait "$p" || true; done
  chmod -R a+rX "$SKILLS_HOME" 2>/dev/null || true
}

if [ "$SKILLS_ONLY" = "1" ]; then
  fetch_skills
  say "skills are in $SKILLS_HOME (log: $LOG)"
  exit 0
fi

# ---------------------------------------------------------------------------------------------
# Downloads that do not need apt run first, in the background, while apt installs libraries.
DL="${TMPDIR:-/tmp}/skyways-dl"; mkdir -p "$DL"

CFT_VERSION="${CFT_VERSION:-154.0.8037.92}"   # Chrome for Testing, stable on 2 October 2026
latest="$(curl -fsS --max-time 8 https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE 2>/dev/null || true)"
if [[ "$latest" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then CFT_VERSION="$latest"; fi

need_chrome=1
if [ -x /opt/chrome-linux64/chrome ] && [ -f /opt/chrome-linux64/.version ] && [ "$(cat /opt/chrome-linux64/.version)" = "$CFT_VERSION" ]; then need_chrome=0; fi
if [ "$need_chrome" = "1" ]; then
  ( curl -fsSL --retry 3 --max-time 240 -o "$DL/chrome.zip" \
      "https://storage.googleapis.com/chrome-for-testing-public/$CFT_VERSION/linux64/chrome-linux64.zip" \
    && echo ok > "$DL/chrome.done" ) >>"$LOG" 2>&1 &
  CHROME_PID=$!
fi

if ! command -v aws >/dev/null 2>&1; then
  ( curl -fsSL --retry 3 --max-time 240 -o "$DL/awscliv2.zip" https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip \
    && echo ok > "$DL/aws.done" ) >>"$LOG" 2>&1 &
  AWS_PID=$!
fi

fetch_skills & SKILLS_PID=$!

# ---------------------------------------------------------------------------------------------
# Libraries Chrome needs on Ubuntu 24.04, fonts for screenshots, and unzip.
APT_PKGS="ca-certificates unzip fontconfig fonts-liberation fonts-dejavu-core fonts-noto-color-emoji \
libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 libatspi2.0-0t64 libcairo2 libcups2t64 libdbus-1-3 \
libdrm2 libgbm1 libglib2.0-0t64 libgtk-3-0t64 libnspr4 libnss3 libpango-1.0-0 libx11-6 libx11-xcb1 libxcb1 \
libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 libxshmfence1 libvulkan1 xdg-utils"
if [ "$SUDO" != "none" ]; then
  export DEBIAN_FRONTEND=noninteractive
  as_root apt-get update -qq >>"$LOG" 2>&1 || say "apt: update failed"
  # shellcheck disable=SC2086
  if ! as_root apt-get install -y -qq --no-install-recommends $APT_PKGS >>"$LOG" 2>&1; then
    say "apt: one batch failed, installing one by one"
    for p in $APT_PKGS; do as_root apt-get install -y -qq --no-install-recommends "$p" >>"$LOG" 2>&1 || say "apt: no $p"; done
  fi
  say "apt: libraries and fonts done"
else
  say "apt: skipped (not root and no sudo)"
fi

# ---------------------------------------------------------------------------------------------
# Chrome for Testing in /opt/chrome-linux64, started through a wrapper that adds the two flags a
# container needs (no sandbox when running as root, no reliance on a small /dev/shm).
if [ "$need_chrome" = "1" ]; then
  wait "${CHROME_PID:-0}" 2>/dev/null || true
  if [ -f "$DL/chrome.done" ] && as_root true; then
    as_root rm -rf /opt/chrome-linux64 \
      && as_root unzip -q -o "$DL/chrome.zip" -d /opt >>"$LOG" 2>&1 \
      && echo "$CFT_VERSION" | as_root tee /opt/chrome-linux64/.version >/dev/null \
      && say "chrome: Chrome for Testing $CFT_VERSION unpacked" || say "chrome: unpack failed"
    # Chrome for Testing lists its own Debian dependencies; install any the list above missed.
    if [ -f /opt/chrome-linux64/deb.deps ]; then
      extra="$(sed -E 's/\(.*\)//; s/\|.*//; s/[[:space:]]+//g' /opt/chrome-linux64/deb.deps | grep -E '^[a-z0-9.+-]+$' | sort -u | tr '\n' ' ')"
      # shellcheck disable=SC2086
      [ -n "$extra" ] && as_root apt-get install -y -qq --no-install-recommends $extra >>"$LOG" 2>&1 || true
    fi
  else
    say "chrome: download failed (storage.googleapis.com must be allowed; it is in the Trusted list)"
  fi
fi
if [ -x /opt/chrome-linux64/chrome ] && as_root true; then
  as_root tee /usr/local/bin/google-chrome >/dev/null <<'WRAP'
#!/bin/sh
# Chrome for Testing (installed by .claude/cloud/setup.sh) with the flags a container needs.
exec /opt/chrome-linux64/chrome --no-sandbox --disable-dev-shm-usage "$@"
WRAP
  as_root chmod 755 /usr/local/bin/google-chrome
  ver="$(/usr/local/bin/google-chrome --version 2>>"$LOG" || true)"
  [ -n "$ver" ] && say "chrome: $ver at /usr/local/bin/google-chrome" || say "chrome: installed but did not start (see $LOG)"
fi

# ---------------------------------------------------------------------------------------------
# AWS CLI v2.
if ! command -v aws >/dev/null 2>&1; then
  wait "${AWS_PID:-0}" 2>/dev/null || true
  if [ -f "$DL/aws.done" ] && as_root true; then
    ( cd "$DL" && unzip -q -o awscliv2.zip && as_root ./aws/install --update ) >>"$LOG" 2>&1 \
      && say "aws: $(aws --version 2>&1)" || say "aws: install failed"
  else
    say "aws: download failed or not root"
  fi
else
  say "aws: $(aws --version 2>&1) already present"
fi

# ---------------------------------------------------------------------------------------------
# Playwright WebKit, for checks in Safari's engine. Its browsers come from cdn.playwright.dev, which is not
# in the Trusted list: allow it (Custom network) or use Full network access, otherwise this step is skipped.
if [ "$SUDO" != "none" ] && [ "${SKYWAYS_WEBKIT:-1}" = "1" ]; then
  code="$(curl -s -o /dev/null --max-time 6 -w '%{http_code}' https://cdn.playwright.dev/ 2>/dev/null || echo 000)"
  if [ "$code" != "000" ] && [ "$code" != "403" ]; then
    if timeout 200 bash -c 'npm install -g --silent playwright@latest && playwright install --with-deps webkit' >>"$LOG" 2>&1; then
      say "webkit: $(playwright --version 2>/dev/null) with WebKit installed (module: $(npm root -g)/playwright)"
    else
      say "webkit: install failed or took too long (see $LOG)"
    fi
  else
    say "webkit: skipped, cdn.playwright.dev is not reachable from this network"
  fi
fi

wait "$SKILLS_PID" 2>/dev/null || true
say "skills: sources in $SKILLS_HOME; .claude/cloud/session-start.sh links them when a session starts"
say "done (log: $LOG)"
rm -rf "$DL"
exit 0

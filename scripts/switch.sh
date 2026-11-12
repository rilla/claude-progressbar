#!/bin/sh
# Turns the progress bars on or off for the session that runs it. The
# statusline command starts the plugin only for a session with a flag here.
set -eu

session=${CLAUDE_CODE_SESSION_ID:-}
if [ -z "$session" ]; then
  echo "no CLAUDE_CODE_SESSION_ID: run this from a Claude Code session" >&2
  exit 1
fi
case "$session" in
  *[!A-Za-z0-9_-]*)
    echo "unexpected session id: $session" >&2
    exit 1
    ;;
esac
flags="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/progressbar/on"

case "${1:-}" in
  on)
    mkdir -p "$flags"
    : > "$flags/$session"
    echo "Progress bars on for this session."
    ;;
  off)
    rm -f "$flags/$session"
    echo "Progress bars off for this session."
    ;;
  *)
    echo "usage: switch.sh on|off" >&2
    exit 2
    ;;
esac

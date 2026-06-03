#!/usr/bin/env bash
# q.sh — Exécute UNE requête SQL en LECTURE SEULE sur le Moodle distant, renvoie du JSON.
# La requête est passée en argument OU sur STDIN.
#   tools/q.sh "SELECT 1"
#   echo "SELECT 1" | tools/q.sh
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$DIR/moodle.env"

SQL="${1:-$(cat)}"

printf '%s' "$SQL" | ssh -p "$MOODLE_SSH_PORT" -o BatchMode=yes \
    "$MOODLE_SSH_USER@$MOODLE_SSH_HOST" "php $MOODLE_REMOTE_QUERY" \
    2> >(grep -v -E 'post-quantum|store now|may need|openssh\.com|WARNING|vulnerable|session' >&2)

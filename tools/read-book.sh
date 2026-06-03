#!/usr/bin/env bash
# read-book.sh — Dump (lecture seule) le contenu d'un livre Moodle par son cmid.
# Sert d'ENTRÉE pour rédiger un quiz : ce n'est pas un livrable versionné.
#   tools/read-book.sh 663
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMID="${1:?usage: read-book.sh <cmid>}"

"$DIR/q.sh" "SELECT bc.pagenum, bc.subchapter, bc.title, bc.content
FROM mdl_book_chapters bc
JOIN mdl_course_modules cm ON cm.instance = bc.bookid
JOIN mdl_modules m ON m.id = cm.module AND m.name = 'book'
WHERE cm.id = ${CMID} AND bc.hidden = 0
ORDER BY bc.pagenum, bc.subchapter"

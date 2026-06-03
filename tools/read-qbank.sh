#!/usr/bin/env bash
# read-qbank.sh — Inventaire (lecture seule) de la banque de questions d'un cours.
# Liste les catégories du contexte cours et, par catégorie, les questions existantes.
#   tools/read-qbank.sh 60            # arborescence des catégories du cours 60
#   tools/read-qbank.sh 60 --questions   # + détail des questions (id, type, intitulé)
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSEID="${1:?usage: read-qbank.sh <courseid> [--questions]}"

echo "### Catégories (contexte cours ${COURSEID}) ###"
"$DIR/q.sh" "SELECT qc.id, qc.name, qc.parent,
  (SELECT COUNT(*) FROM mdl_question_bank_entries be WHERE be.questioncategoryid = qc.id) AS nb_questions
FROM mdl_question_categories qc
JOIN mdl_context ctx ON ctx.id = qc.contextid
WHERE ctx.instanceid = ${COURSEID} AND ctx.contextlevel = 50
ORDER BY qc.parent, qc.id"

if [ "${2:-}" = "--questions" ]; then
  echo "### Questions (dernière version de chaque entrée) ###"
  "$DIR/q.sh" "SELECT qc.name AS categorie, q.id AS questionid, q.qtype, q.name AS intitule
FROM mdl_question_categories qc
JOIN mdl_context ctx ON ctx.id = qc.contextid AND ctx.instanceid = ${COURSEID} AND ctx.contextlevel = 50
JOIN mdl_question_bank_entries be ON be.questioncategoryid = qc.id
JOIN mdl_question_versions qv ON qv.questionbankentryid = be.id
  AND qv.version = (SELECT MAX(v2.version) FROM mdl_question_versions v2 WHERE v2.questionbankentryid = be.id)
JOIN mdl_question q ON q.id = qv.questionid
ORDER BY qc.name, q.id"
fi

# CLAUDE.md — consignes projet Moodle (ericm.fr/elearning)

Instructions à respecter pour ce dépôt. Voir aussi `README.md` (vue d'ensemble)
et `tools/README.md` (outillage).

## Règle n°1 — LECTURE SEULE dans Moodle

On ne **lit** que dans Moodle (base, fichiers), **jamais on n'écrit**.
Aucune écriture base / fichiers / config, pas de `moosh` en écriture, pas de
Web Services en écriture. `tools/moodle-query.php` refuse tout sauf
`SELECT/SHOW/DESCRIBE/EXPLAIN`. Les livrables sont **importés à la main** par
l'enseignant.

## Livrables produits

| Contenu | Format | Dossier |
|---|---|---|
| Quizz | Moodle XML | `quizz/` |
| Livres / leçons / devoirs… | `.mbz` (backup 4.1) | `backups/` |

Le repo contient **uniquement les fichiers générés** + l'outillage de lecture —
ce n'est pas un miroir du site. Ne pas exporter/dupliquer le contenu existant.
Ne pas toucher à `css/` ni `gestionProjet/` (possiblement hot-linkés dans Moodle).

## Conventions

- **Nommage des questions** : `THEME-NN-TYPE` (`DFS-01-QCM`, `RAID-07-VF`).
  `QCM`=choix multiple · `VF`=vrai/faux · `RC`=réponse courte · `APP`=appariement · `CLOZE`=réponses intégrées.
- **Import XML** : penser à cocher *« Récupérer la catégorie depuis le fichier »*.
- **Cloze** : à tester à l'import (syntaxe non vérifiable hors Moodle).
- **Commits** : directement sur `main`, en français.

## Accès serveur (lecture seule)

- SSH `admin1@212.129.63.245` port **8822** (Debian 11, `srv-deb11`).
- Lecteur SQL : `/home/admin1/moodle-query.php` (source dans `tools/`).
  Redéploiement : `scp -P 8822 tools/moodle-query.php admin1@212.129.63.245:/home/admin1/moodle-query.php`
- Moodle **4.1**, base MariaDB `moodle`, préfixe `mdl_`. Identifiants lus côté
  serveur depuis `config.php` — **aucun secret dans ce repo**.
- Repères : contexte cours = `mdl_context.contextlevel=50`. Exemple : `cmid 663`
  = livre DFS, cours **60** « ISCE 25-27 Bloc 1-2 ».

---

## Annotations (notes de l'enseignant)

> Section libre : ajoute ici tes consignes, préférences, retours. Je les relis
> à chaque session et je les applique.

- _(rien pour l'instant)_

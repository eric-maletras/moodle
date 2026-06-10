# tools/ — Outillage Moodle (LECTURE SEULE)

Outils pour lire le Moodle de `ericm.fr/elearning` et produire des livrables à
importer **manuellement** dans Moodle.

> ⚠️ **Règle absolue : on ne fait QUE lire dans Moodle, jamais écrire.**
> Aucun script ici ne modifie la base, les fichiers ou la config de Moodle.
> Les livrables produits sont importés à la main par l'enseignant.

## Livrables produits

| Type de contenu | Format livré | Import dans Moodle |
|---|---|---|
| Quizz | **Moodle XML** | Banque de questions → Importer |
| Le reste (livres, leçons, devoirs…) | **`.mbz`** (backup Moodle 4.1) | Restauration |

## Pré-requis

- Accès SSH au serveur (voir `moodle.env`).
- `moodle-query.php` déployé dans le home de l'utilisateur SSH sur le serveur.
- Les scripts `.sh` se lancent depuis un environnement bash (Git Bash / WSL).

### (Re)déployer le lecteur SQL sur le serveur

```bash
scp -P 8822 tools/moodle-query.php admin1@212.129.63.245:~/moodle-query.php
```

## Scripts

| Script | Rôle |
|---|---|
| `moodle-query.php` | Lecteur SQL **read-only** (refuse tout sauf SELECT/SHOW/DESCRIBE/EXPLAIN). Tourne sur le serveur. |
| `q.sh` | Envoie une requête SQL au serveur et renvoie le JSON. `tools/q.sh "SELECT 1"` |
| `read-book.sh <cmid>` | Dump le contenu d'un livre (entrée pour rédiger un quiz). |
| `read-qbank.sh <courseid> [--questions]` | Inventaire de la banque de questions d'un cours. |
| `build-book-mbz.py` | Génère un `.mbz` (backup activité « Livre », Moodle 4.1) à partir d'un JSON de chapitres `[{id,title,contents}]`. Aucune écriture Moodle. |

## Workflow type : un livre → un quiz

1. Lire le livre : `tools/read-book.sh 663`
2. Inventorier les questions existantes : `tools/read-qbank.sh 60 --questions`
3. Rédiger / compléter le quiz → fichier **Moodle XML** dans `cours/<cours>/quiz/`.
4. L'enseignant importe le XML dans la banque de questions, puis crée le quiz.

## Repères

- Moodle **4.1**, base MariaDB `moodle`, préfixe `mdl_`.
- Contexte d'un cours : `mdl_context.contextlevel = 50`, `instanceid = <courseid>`.
- Exemple de référence : `cmid 663` = livre « système de fichiers distribué »,
  cours **60** « ISCE 25-27 Bloc 1-2 ».

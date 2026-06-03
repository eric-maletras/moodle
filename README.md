# moodle — contenus & outillage pour ericm.fr/elearning

Dépôt de travail pour le Moodle **http://www.ericm.fr/elearning** (Moodle 4.1).
On y versionne **les fichiers générés** (quizz, backups) et **l'outillage de lecture**
du site. Le repo n'est **pas** un miroir/backup du Moodle.

## ⚠️ Règle absolue : lecture seule

On ne fait **que lire** dans Moodle (base de données, fichiers) — **jamais écrire**.
Les livrables produits ici sont **importés à la main** dans Moodle par l'enseignant.

| Type de contenu | Livrable produit | Import dans Moodle |
|---|---|---|
| Quizz | **Moodle XML** (`quizz/`) | Banque de questions → Importer |
| Le reste (livres, leçons, devoirs…) | **`.mbz`** (`backups/`) | Restauration |

## Reprendre le projet

Le projet est cloné en local dans `C:\users\eric\github\moodle`.
Depuis `github/` :

```powershell
cd moodle
```

## Structure

```
moodle/
├── tools/        Outillage de LECTURE (voir tools/README.md)
├── quizz/        Livrables Moodle XML (1 fichier par test)
├── backups/      Livrables .mbz (livres, leçons, devoirs…)
├── css/          Feuilles de style des leçons (existant, ne pas déplacer)
└── gestionProjet/ Ressources de cours (existant, ne pas déplacer)
```

> `css/` et `gestionProjet/` sont potentiellement liés en dur (hot-link) depuis
> des pages Moodle : **ne pas les renommer ni les déplacer** sans vérifier les
> références dans la base.

## Workflow type : un livre → un quizz

1. Lire le livre source : `tools/read-book.sh <cmid>`
2. Inventorier les questions existantes : `tools/read-qbank.sh <courseid> --questions`
3. Rédiger / compléter le quizz → fichier **Moodle XML** dans `quizz/`
4. L'enseignant importe le XML (cocher *« Récupérer la catégorie depuis le fichier »*).

## Accès serveur (lecture seule)

- SSH : `admin1@212.129.63.245` port **8822** (Debian 11 `srv-deb11`).
- Lecteur SQL read-only `moodle-query.php` déployé dans `/home/admin1/`
  (source versionnée dans `tools/`, redéployable via `tools/README.md`).
- Base MariaDB `moodle`, préfixe `mdl_`. Identifiants lus côté serveur depuis
  le `config.php` de Moodle — **aucun secret n'est stocké dans ce repo**.

## Convention de nommage des questions

`THEME-NN-TYPE` (ex. `DFS-01-QCM`, `RAID-07-VF`) :
`QCM` = choix multiple · `VF` = vrai/faux · `RC` = réponse courte ·
`APP` = appariement · `CLOZE` = réponses intégrées.

#!/usr/bin/env python3
# tools/build-quiz-linux-debian.py
# Compose un test de 25 questions (Moodle XML) « sur le cours Linux-Debian » :
#   - 12 questions issues de la leçon initiale (cmid 20), reconverties ;
#   - 13 questions sélectionnées (on-topic, dédupliquées) dans le banc fourni
#     (backups/questions-ISCE 25-27 Bloc 1-2-II.1 Linux-...xml), copiées verbatim.
# Aucune écriture Moodle : produit juste un fichier XML à importer à la main.

import re
import sys
import unicodedata

BANK = "backups/questions-ISCE 25-27 Bloc 1-2-II.1 Linux-20260610-1710.xml"
OUT = "quizz/test-linux-debian-25.xml"

# Noms (préfixe normalisé) des questions à reprendre du banc, dans l'ordre.
BANK_TARGETS = [
    "racine linux",
    "repertoire config linux",
    "debian est une distribution commerciale",
    "editeur par defaut",
    "chmod",
    "linux cd",
    "linux cp",
    "mv",
    "linux apt install",
    "linux apt update",
    "apt upgrade",
    "copier dossier recursivement",
]

# Variantes de réponse à ajouter à certaines questions « commande » du banc
# (réponse courte = correspondance exacte → on rend l'évaluation plus tolérante).
BANK_VARIANTS = {
    "copier dossier recursivement": [
        "cp -R Documents Sauvegarde",
        "cp -r Documents/ Sauvegarde",
        "cp -r Documents Sauvegarde/",
        "cp -r Documents/ Sauvegarde/",
        "cp -r* Documents* Sauvegarde*",
        "cp -R* Documents* Sauvegarde*",
    ],
}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"\s+", " ", s)


def extract_bank(path, targets):
    s = open(path, encoding="utf-8").read()
    blocks = re.findall(r'<question type="(?!category)[^"]+">.*?</question>', s, re.S)
    by_name = []
    for b in blocks:
        m = re.search(r"<name>\s*<text>(.*?)</text>", b, re.S)
        by_name.append((norm(m.group(1)) if m else "", b))
    chosen = []
    used = set()
    for t in targets:
        for i, (n, b) in enumerate(by_name):
            if i in used:
                continue
            if n.startswith(t):
                block = b.strip()
                if t in BANK_VARIANTS:
                    block = add_sa_variants(block, BANK_VARIANTS[t])
                chosen.append(block)
                used.add(i)
                break
        else:
            print(f"!! cible banc introuvable: {t}", file=sys.stderr)
    return chosen


def add_sa_variants(block, variants):
    # Insère des <answer fraction="100"> supplémentaires avant </question>.
    ins = "\n".join(
        f'    <answer fraction="100" format="moodle_auto_format"><text>{v}</text>'
        f'<feedback format="moodle_auto_format"><text></text></feedback></answer>'
        for v in variants
    )
    return block.replace("</question>", ins + "\n  </question>")


# ---------- Helpers de génération (questions de la leçon) ----------

def _wrap(q):
    return q.strip() + "\n"


def sa(name, qtext, answers, usecase=0):
    a = "\n".join(
        f'    <answer fraction="100" format="moodle_auto_format"><text>{x}</text>'
        f'<feedback format="html"><text></text></feedback></answer>'
        for x in answers
    )
    return _wrap(f'''<question type="shortanswer">
    <name><text>{name}</text></name>
    <questiontext format="html"><text><![CDATA[{qtext}]]></text></questiontext>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <usecase>{usecase}</usecase>
{a}
  </question>''')


def numeric(name, qtext, value, tol=0):
    return _wrap(f'''<question type="numerical">
    <name><text>{name}</text></name>
    <questiontext format="html"><text><![CDATA[{qtext}]]></text></questiontext>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <answer fraction="100" format="moodle_auto_format"><text>{value}</text>
      <feedback format="html"><text></text></feedback><tolerance>{tol}</tolerance></answer>
  </question>''')


def vf(name, qtext, correct_true, generalfeedback=""):
    tf = ("true", "false") if correct_true else ("false", "true")
    gf = (f'\n    <generalfeedback format="html"><text><![CDATA[{generalfeedback}]]></text>'
          f'</generalfeedback>' if generalfeedback else "")
    return _wrap(f'''<question type="truefalse">
    <name><text>{name}</text></name>
    <questiontext format="html"><text><![CDATA[{qtext}]]></text></questiontext>{gf}
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>1.0000000</penalty>
    <hidden>0</hidden>
    <answer fraction="100" format="moodle_auto_format"><text>{tf[0]}</text><feedback format="html"><text>Correct.</text></feedback></answer>
    <answer fraction="0" format="moodle_auto_format"><text>{tf[1]}</text><feedback format="html"><text>Incorrect.</text></feedback></answer>
  </question>''')


def mc(name, qtext, options, single=True):
    # options : liste de (texte, fraction)
    ans = "\n".join(
        f'    <answer fraction="{frac}" format="html"><text><![CDATA[{txt}]]></text>'
        f'<feedback format="html"><text></text></feedback></answer>'
        for txt, frac in options
    )
    return _wrap(f'''<question type="multichoice">
    <name><text>{name}</text></name>
    <questiontext format="html"><text><![CDATA[{qtext}]]></text></questiontext>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>{"true" if single else "false"}</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>abc</answernumbering>
    <correctfeedback format="html"><text>Bonne réponse.</text></correctfeedback>
    <partiallycorrectfeedback format="html"><text>Partiellement correct.</text></partiallycorrectfeedback>
    <incorrectfeedback format="html"><text>Réponse incorrecte.</text></incorrectfeedback>
{ans}
  </question>''')


def matching(name, qtext, pairs):
    subs = "\n".join(
        f'    <subquestion format="html"><text><![CDATA[{p}]]></text>'
        f'<answer><text>{a}</text></answer></subquestion>'
        for p, a in pairs
    )
    return _wrap(f'''<question type="matching">
    <name><text>{name}</text></name>
    <questiontext format="html"><text><![CDATA[{qtext}]]></text></questiontext>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <shuffleanswers>true</shuffleanswers>
    <correctfeedback format="html"><text>Bonne réponse.</text></correctfeedback>
    <partiallycorrectfeedback format="html"><text>Partiellement correct.</text></partiallycorrectfeedback>
    <incorrectfeedback format="html"><text>Réponse incorrecte.</text></incorrectfeedback>
{subs}
  </question>''')


def lesson_questions():
    q = []
    q.append(sa("LIN-01-RC Origine des OS",
                "<p>Quel système d'exploitation est à l'origine de la quasi-totalité des OS ?</p>",
                ["UNIX", "Unix", "unix"]))
    q.append(numeric("LIN-02-NUM Date du projet GNU",
                     "<p>En quelle année le projet GNU a-t-il été créé par Richard Stallman ?</p>", 1984))
    q.append(mc("LIN-03-QCM Rôles préinstallés",
                "<p>Dans une distribution Linux, quels rôles serveurs sont préinstallés par défaut ?</p>",
                [("Aucun : il faut installer chaque service au besoin.", 100),
                 ("DHCP - DNS", 0), ("DHCP - FTP - DNS", 0), ("FTP - IIS", 0)]))
    q.append(vf("LIN-04-VF Noyau Linux totalement libre",
                "<p>Le noyau Linux est-il <strong>totalement</strong> libre ?</p>", correct_true=False))
    q.append(mc("LIN-05-QCM Distributions grand public",
                "<p>Parmi ces distributions, lesquelles sont orientées <strong>grand public</strong> ?</p>",
                [("Ubuntu", 50), ("Fedora", 50),
                 ("Debian", -50), ("Red Hat Enterprise Linux", -50), ("Slackware", -50)], single=False))
    q.append(matching("LIN-06-APP Arborescence Debian",
                      "<p>Associez chaque dossier à son contenu.</p>",
                      [("Les fichiers exécutables et les commandes", "bin"),
                       ("Les fichiers de configuration", "etc"),
                       ("Les données variables", "var")]))
    q.append(matching("LIN-07-APP Commandes de droits",
                      "<p>Associez chaque commande à son action.</p>",
                      [("Changer le propriétaire", "chown"),
                       ("Changer les permissions", "chmod"),
                       ("Changer le groupe propriétaire", "chgrp")]))
    q.append(sa("LIN-08-RC chmod (droit d'exécution au groupe)",
                "<p>On veut donner au groupe propriétaire le droit d'exécution sur le fichier "
                "<code>text.php</code>. Quelle est la commande ?</p>",
                ["chmod g+x text.php", "chmod g+x ./text.php", "chmod*g+x*text.php"]))
    q.append(sa("LIN-09-RC chown récursif",
                "<p>On veut changer le propriétaire et le groupe propriétaire du dossier <code>glpi</code> "
                "et de tout son contenu (récursif), vers <code>www-data:www-data</code>. Quelle est la commande ?</p>",
                ["chown -R www-data:www-data glpi", "chown www-data:www-data -R glpi",
                 "chown -R www-data:www-data ./glpi", "chown*-R*www-data:www-data*glpi",
                 "chown*www-data:www-data*-R*glpi"]))
    q.append(sa("LIN-10-RC Lister avec permissions",
                "<p>On veut lister les fichiers/répertoires du dossier courant <strong>en affichant les "
                "permissions</strong>. Quelle est la commande ?</p>",
                ["ls -l", "ls -al", "ls -la", "ls -lh", "ll", "ls -l *"]))
    q.append(sa("LIN-11-RC Lister un dossier précis",
                "<p>Le dossier courant est <code>/home/admin1</code>. On veut lister (avec les permissions) "
                "le dossier <code>/var/www</code>. Quelle est la commande ?</p>",
                ["ls -l /var/www", "ls -al /var/www", "ls -la /var/www", "ls -l /var/www/",
                 "ls -l* /var/www*", "ls -al* /var/www*"]))
    q.append(matching("LIN-12-APP Commandes usuelles",
                      "<p>Associez chaque commande à son action (dossier courant).</p>",
                      [("Créer un dossier <code>temp</code> dans le dossier courant", "mkdir temp"),
                       ("Copier <code>fic2.txt</code> vers le sous-dossier <code>dossier1</code>", "cp fic2.txt dossier1/"),
                       ("Copier <code>fic2.txt</code> vers <code>/var/www/dossier1</code>", "cp fic2.txt /var/www/dossier1/"),
                       ("Déplacer <code>fic2.txt</code> vers le sous-dossier <code>dossier1</code>", "mv fic2.txt dossier1/fic2.txt")]))
    q.append(vf("LIN-13-VF Distribution = GNU + Linux ?",
                "<p>Une distribution Linux est-elle <strong>forcément</strong> composée d'une partie GNU "
                "<strong>et</strong> d'une partie Linux ?</p>",
                correct_true=False,
                generalfeedback="<p>Non : les parties GNU et Linux sont indépendantes. Il existe des systèmes "
                "avec Linux sans GNU (ex. <strong>Android</strong>) et des systèmes GNU sans Linux "
                "(ex. GNU/Hurd).</p>"))
    return q


def main():
    lesson = lesson_questions()
    bank = extract_bank(BANK, BANK_TARGETS)
    total = len(lesson) + len(bank)

    header = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  Test « Linux-Debian Généralités » — {total} questions.
  Source : {len(lesson)} questions reprises de la leçon initiale (cmid 20),
           {len(bank)} questions sélectionnées dans le banc II.1 Linux (on-topic).
  Import : Banque de questions > Importer > « Format XML Moodle »
           (cocher « Récupérer la catégorie depuis le fichier »).
-->
<quiz>

  <question type="category">
    <category><text>$course$/top/Test - Linux-Debian Généralités</text></category>
    <info format="html"><text>Test de {total} questions sur le cours Linux-Debian (généralités, distributions, droits, système de fichiers, commandes, apt).</text></info>
  </question>

'''
    parts = [header]
    parts.append("  <!-- ===== Questions issues de la leçon initiale ===== -->\n\n")
    for q in lesson:
        parts.append("  " + q + "\n")
    parts.append("  <!-- ===== Questions reprises du banc II.1 Linux ===== -->\n\n")
    for b in bank:
        parts.append("  " + b + "\n\n")
    parts.append("</quiz>\n")

    open(OUT, "w", encoding="utf-8").write("".join(parts))
    print(f"OK : {OUT} — {total} questions ({len(lesson)} leçon + {len(bank)} banc)")


if __name__ == "__main__":
    main()

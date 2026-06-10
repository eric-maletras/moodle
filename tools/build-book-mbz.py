#!/usr/bin/env python3
# tools/build-book-mbz.py
# Génère un backup Moodle 4.1 (.mbz) d'un module « Livre » à partir d'un JSON
# de chapitres [{"id","title","contents"}], dans l'ordre fourni.
#
# LECTURE SEULE côté Moodle : ce script ne touche pas au serveur, il assemble
# juste un fichier .mbz local (tar.gz) à importer/restaurer manuellement.
#
# Usage :
#   python tools/build-book-mbz.py --chapters /tmp/chapitres.json \
#       --name "Linux-Debian Généralités" --out backups/livre-xxx.mbz
#
# Le .mbz est un backup d'ACTIVITÉ (type=activity) : à restaurer dans un cours
# via « Restauration » → « Importer dans un cours existant ».

import argparse
import gzip
import hashlib
import io
import json
import os
import tarfile
import time

# --- Identifiants synthétiques (remappés par Moodle à la restauration) ---
BOOK_INSTANCE_ID = 9999
MODULE_ID = 20          # cmid d'origine (informatif)
CONTEXT_ID = 5453       # contexte module d'origine (informatif)
SECTION_ID = 36
CHAPTER_ID_BASE = 9000

# --- Métadonnées du site/cours d'origine (informatives) ---
WWWROOT = "http://www.ericm.fr/elearning"
ORIG_COURSE_ID = 10
ORIG_COURSE_CTX = 5443
ORIG_SYSTEM_CTX = 1
ORIG_COURSE_FORMAT = "topics"
ORIG_COURSE_FULLNAME = "liste Leçon/Atelier Bloc 1"
ORIG_COURSE_SHORTNAME = "liste Leçon/Atelier Bloc 1"
ORIG_COURSE_STARTDATE = 1679785200

# --- Versions Moodle 4.1 ---
MOODLE_VERSION = "2022112800"
MOODLE_RELEASE = "4.1"
BACKUP_VERSION = "2022112800"
BACKUP_RELEASE = "4.1"

# Ordre de navigation des chapitres (ids de pages de la leçon source).
DEFAULT_ORDER = [50, 64, 65, 52, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def cdata(s: str) -> str:
    # Sécurise un éventuel ]]> dans le contenu HTML.
    return "<![CDATA[" + s.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def clean_html(s: str) -> str:
    # Corrige les artefacts d'encodage de la source (U+001C à la place de « fi »).
    s = s.replace("\x1c", "fi").replace("fifichier", "fichier")
    # Retire la consigne de navigation propre à la leçon.
    s = s.replace("Cliquer sur Fin de la leçon", "").replace("Cliquer sur Fin de la leçon", "")
    return s.strip()


def build_book_xml(name, chapters, now):
    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append(f'<activity id="{BOOK_INSTANCE_ID}" moduleid="{MODULE_ID}" '
               f'modulename="book" contextid="{CONTEXT_ID}">')
    out.append(f'  <book id="{BOOK_INSTANCE_ID}">')
    out.append(f'    <name>{esc(name)}</name>')
    out.append('    <intro></intro>')
    out.append('    <introformat>1</introformat>')
    out.append('    <numbering>1</numbering>')
    out.append('    <navstyle>1</navstyle>')
    out.append('    <customtitles>0</customtitles>')
    out.append('    <revision>1</revision>')
    out.append(f'    <timecreated>{now}</timecreated>')
    out.append(f'    <timemodified>{now}</timemodified>')
    out.append('    <chapters>')
    for i, ch in enumerate(chapters, start=1):
        cid = CHAPTER_ID_BASE + i
        out.append(f'      <chapter id="{cid}">')
        out.append(f'        <pagenum>{i}</pagenum>')
        out.append('        <subchapter>0</subchapter>')
        out.append(f'        <title>{esc(ch["title"])}</title>')
        out.append(f'        <content>{cdata(ch["contents"])}</content>')
        out.append('        <contentformat>1</contentformat>')
        out.append('        <hidden>0</hidden>')
        out.append(f'        <timecreated>{now}</timecreated>')
        out.append(f'        <timemodified>{now}</timemodified>')
        out.append('        <importsrc></importsrc>')
        out.append('      </chapter>')
    out.append('    </chapters>')
    out.append('  </book>')
    out.append('</activity>')
    return "\n".join(out) + "\n"


def build_module_xml(now):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<module id="{MODULE_ID}" version="{MOODLE_VERSION}">
  <modulename>book</modulename>
  <sectionid>{SECTION_ID}</sectionid>
  <sectionnumber>1</sectionnumber>
  <idnumber></idnumber>
  <added>{now}</added>
  <score>0</score>
  <indent>0</indent>
  <visible>1</visible>
  <visibleoncoursepage>1</visibleoncoursepage>
  <visibleold>1</visibleold>
  <groupmode>0</groupmode>
  <groupingid>0</groupingid>
  <completion>0</completion>
  <completiongradeitemnumber>$@NULL@$</completiongradeitemnumber>
  <completionpassgrade>0</completionpassgrade>
  <completionview>0</completionview>
  <completionexpected>0</completionexpected>
  <availability>$@NULL@$</availability>
  <showdescription>0</showdescription>
  <downloadcontent>1</downloadcontent>
  <tags></tags>
</module>
'''


def build_inforef_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<inforef>
  <fileref></fileref>
</inforef>
'''


def build_activity_roles_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<roles>
  <role_overrides></role_overrides>
  <role_assignments></role_assignments>
</roles>
'''


def build_grades_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<activity_gradebook>
  <grade_items></grade_items>
  <grade_letters></grade_letters>
</activity_gradebook>
'''


def build_grade_history_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<grade_history>
  <grade_grades></grade_grades>
</grade_history>
'''


def build_calendar_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<calendar>
  <events></events>
</calendar>
'''


def build_comments_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<comments></comments>
'''


def build_competencies_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<course_module_competencies>
  <competencies></competencies>
</course_module_competencies>
'''


def build_filters_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<filters>
  <filter_actives></filter_actives>
  <filter_configs></filter_configs>
</filters>
'''


def build_root_files_xml():
    return '<?xml version="1.0" encoding="UTF-8"?>\n<files>\n</files>\n'


def build_scales_xml():
    return '<?xml version="1.0" encoding="UTF-8"?>\n<scales_definition>\n</scales_definition>\n'


def build_outcomes_xml():
    return '<?xml version="1.0" encoding="UTF-8"?>\n<outcomes_definition>\n</outcomes_definition>\n'


def build_questions_xml():
    return '<?xml version="1.0" encoding="UTF-8"?>\n<question_categories>\n</question_categories>\n'


def build_groups_xml():
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<groups>\n'
            '  <groupcustomfields></groupcustomfields>\n'
            '  <groupings></groupings>\n</groups>\n')


def build_roles_definition_xml():
    roles = [
        (1, "manager", "manager", 1),
        (2, "coursecreator", "coursecreator", 2),
        (3, "editingteacher", "editingteacher", 3),
        (4, "teacher", "teacher", 4),
        (5, "student", "student", 5),
        (6, "guest", "guest", 6),
        (7, "user", "user", 7),
        (8, "frontpage", "frontpage", 8),
    ]
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<roles_definition>']
    for rid, shortname, archetype, sort in roles:
        out.append(f'  <role id="{rid}">')
        out.append('    <name></name>')
        out.append(f'    <shortname>{shortname}</shortname>')
        out.append('    <nameincourse>$@NULL@$</nameincourse>')
        out.append('    <description></description>')
        out.append(f'    <sortorder>{sort}</sortorder>')
        out.append(f'    <archetype>{archetype}</archetype>')
        out.append('  </role>')
    out.append('</roles_definition>')
    return "\n".join(out) + "\n"


def build_moodle_backup_xml(name, now, backup_id, site_hash):
    activity_dir = f"book_{MODULE_ID}"
    root_settings = [
        ("filename", f"backup-moodle2-activity-{MODULE_ID}-book.mbz"),
        ("imscc11", "0"),
        ("users", "0"),
        ("anonymize", "0"),
        ("role_assignments", "0"),
        ("activities", "1"),
        ("blocks", "1"),
        ("files", "1"),
        ("filters", "1"),
        ("comments", "0"),
        ("badges", "0"),
        ("calendarevents", "0"),
        ("userscompletion", "0"),
        ("logs", "0"),
        ("grade_histories", "0"),
        ("questionbank", "0"),
        ("groups", "0"),
        ("competencies", "1"),
        ("customfield", "1"),
        ("contentbankcontent", "1"),
        ("xapistate", "1"),
        ("legacyfiles", "0"),
    ]
    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<moodle_backup>')
    out.append('  <information>')
    out.append(f'    <name>backup-moodle2-activity-{MODULE_ID}-book.mbz</name>')
    out.append(f'    <moodle_version>{MOODLE_VERSION}</moodle_version>')
    out.append(f'    <moodle_release>{MOODLE_RELEASE}</moodle_release>')
    out.append(f'    <backup_version>{BACKUP_VERSION}</backup_version>')
    out.append(f'    <backup_release>{BACKUP_RELEASE}</backup_release>')
    out.append(f'    <backup_date>{now}</backup_date>')
    out.append('    <mnet_remoteusers>0</mnet_remoteusers>')
    out.append('    <include_files>1</include_files>')
    out.append('    <include_file_references_to_external_content>0</include_file_references_to_external_content>')
    out.append(f'    <original_wwwroot>{WWWROOT}</original_wwwroot>')
    out.append(f'    <original_site_identifier_hash>{site_hash}</original_site_identifier_hash>')
    out.append(f'    <original_course_id>{ORIG_COURSE_ID}</original_course_id>')
    out.append(f'    <original_course_format>{ORIG_COURSE_FORMAT}</original_course_format>')
    out.append(f'    <original_course_fullname>{esc(ORIG_COURSE_FULLNAME)}</original_course_fullname>')
    out.append(f'    <original_course_shortname>{esc(ORIG_COURSE_SHORTNAME)}</original_course_shortname>')
    out.append(f'    <original_course_startdate>{ORIG_COURSE_STARTDATE}</original_course_startdate>')
    out.append(f'    <original_course_contextid>{ORIG_COURSE_CTX}</original_course_contextid>')
    out.append(f'    <original_system_contextid>{ORIG_SYSTEM_CTX}</original_system_contextid>')
    out.append('    <details>')
    out.append(f'      <detail backup_id="{backup_id}">')
    out.append('        <type>activity</type>')
    out.append('        <format>moodle2</format>')
    out.append('        <interactive>1</interactive>')
    out.append('        <mode>10</mode>')
    out.append('        <execution>1</execution>')
    out.append('        <executiontime>0</executiontime>')
    out.append('      </detail>')
    out.append('    </details>')
    out.append('    <contents>')
    out.append('      <activities>')
    out.append('        <activity>')
    out.append(f'          <moduleid>{MODULE_ID}</moduleid>')
    out.append(f'          <sectionid>{SECTION_ID}</sectionid>')
    out.append('          <modulename>book</modulename>')
    out.append(f'          <title>{esc(name)}</title>')
    out.append(f'          <directory>activities/{activity_dir}</directory>')
    out.append('        </activity>')
    out.append('      </activities>')
    out.append('      <settings>')
    for n, v in root_settings:
        out.append('        <setting>')
        out.append('          <level>root</level>')
        out.append(f'          <name>{n}</name>')
        out.append(f'          <value>{esc(str(v))}</value>')
        out.append('        </setting>')
    for n, v in [("included", "1"), ("userinfo", "0")]:
        out.append('        <setting>')
        out.append('          <level>activity</level>')
        out.append(f'          <activity>{activity_dir}</activity>')
        out.append(f'          <name>{activity_dir}_{n}</name>')
        out.append(f'          <value>{v}</value>')
        out.append('        </setting>')
    out.append('      </settings>')
    out.append('    </contents>')
    out.append('  </information>')
    out.append('</moodle_backup>')
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--order", default=",".join(str(x) for x in DEFAULT_ORDER))
    args = ap.parse_args()

    with open(args.chapters, encoding="utf-8") as f:
        rows = json.load(f)
    by_id = {int(r["id"]): r for r in rows}
    order = [int(x) for x in args.order.split(",")]

    chapters = []
    for pid in order:
        r = by_id[pid]
        chapters.append({"title": r["title"].strip(), "contents": clean_html(r["contents"])})

    now = int(time.time())
    backup_id = hashlib.md5(f"{args.name}{now}".encode()).hexdigest()
    site_hash = hashlib.md5(WWWROOT.encode()).hexdigest()

    activity_dir = f"activities/book_{MODULE_ID}"
    files = {
        "moodle_backup.xml": build_moodle_backup_xml(args.name, now, backup_id, site_hash),
        "files.xml": build_root_files_xml(),
        "scales.xml": build_scales_xml(),
        "outcomes.xml": build_outcomes_xml(),
        "questions.xml": build_questions_xml(),
        "groups.xml": build_groups_xml(),
        "roles.xml": build_roles_definition_xml(),
        f"{activity_dir}/book.xml": build_book_xml(args.name, chapters, now),
        f"{activity_dir}/module.xml": build_module_xml(now),
        f"{activity_dir}/inforef.xml": build_inforef_xml(),
        f"{activity_dir}/roles.xml": build_activity_roles_xml(),
        f"{activity_dir}/grades.xml": build_grades_xml(),
        f"{activity_dir}/grade_history.xml": build_grade_history_xml(),
        f"{activity_dir}/calendar.xml": build_calendar_xml(),
        f"{activity_dir}/comments.xml": build_comments_xml(),
        f"{activity_dir}/competencies.xml": build_competencies_xml(),
        f"{activity_dir}/filters.xml": build_filters_xml(),
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    # .mbz = tar gzippé, fichiers à la racine de l'archive.
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tar:
        for path, content in files.items():
            data = content.encode("utf-8")
            info = tarfile.TarInfo(name=path)
            info.size = len(data)
            info.mtime = now
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(data))
    with gzip.open(args.out, "wb") as gz:
        gz.write(raw.getvalue())

    print(f"OK : {args.out}  ({len(chapters)} chapitres, {len(files)} fichiers)")


if __name__ == "__main__":
    main()

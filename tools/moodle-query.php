<?php
/**
 * moodle-query.php — Lecteur SQL STRICTEMENT EN LECTURE SEULE pour le Moodle d'ericm.fr.
 *
 * - Lit les identifiants de la base depuis le config.php de Moodle (jamais en dur ici).
 * - Reçoit UNE requête SQL sur STDIN.
 * - N'autorise QUE SELECT / SHOW / DESCRIBE / EXPLAIN, une seule instruction.
 * - Renvoie le résultat en JSON sur STDOUT.
 *
 * Usage (sur le serveur) :
 *   echo "SELECT ..." | php ~/moodle-query.php
 *
 * Règle projet : on ne fait QUE lire dans Moodle, jamais écrire.
 */

$configPath = getenv('MOODLE_CONFIG') ?: '/var/www/html/elearning/config.php';
$src = @file_get_contents($configPath);
if ($src === false) {
    fwrite(STDERR, "ERREUR: config.php introuvable/illisible: $configPath\n");
    exit(1);
}

/** Extrait une valeur de chaîne PHP ($CFG->$k = '...';) en gérant les échappements. */
function cfg($src, $k) {
    // Chaîne entre apostrophes (gère \' et \\)
    if (preg_match('/' . preg_quote($k, '/') . '\s*=\s*\'((?:\\\\.|[^\'\\\\])*)\'/s', $src, $m)) {
        return str_replace(array("\\\\", "\\'"), array("\\", "'"), $m[1]);
    }
    // Chaîne entre guillemets doubles
    if (preg_match('/' . preg_quote($k, '/') . '\s*=\s*"((?:\\\\.|[^"\\\\])*)"/s', $src, $m)) {
        return stripcslashes($m[1]);
    }
    return null;
}

$sql = stream_get_contents(STDIN);
if ($sql === false || trim($sql) === '') {
    fwrite(STDERR, "ERREUR: aucune requête reçue sur STDIN\n");
    exit(1);
}

// --- Garde-fou lecture seule -------------------------------------------------
$probe = rtrim(trim($sql), "; \t\n\r");        // retire les ; finaux
if (strpos($probe, ';') !== false) {            // bloque les requêtes empilées
    fwrite(STDERR, "REFUS: une seule instruction autorisée (point-virgule interne détecté)\n");
    exit(2);
}
if (!preg_match('/^\s*(SELECT|SHOW|DESCRIBE|DESC|EXPLAIN)\b/i', $probe)) {
    fwrite(STDERR, "REFUS: lecture seule — seules SELECT/SHOW/DESCRIBE/EXPLAIN sont autorisées\n");
    exit(2);
}
// ----------------------------------------------------------------------------

$h = cfg($src, 'dbhost');
$n = cfg($src, 'dbname');
$u = cfg($src, 'dbuser');
$p = cfg($src, 'dbpass');

$db = new mysqli($h, $u, $p, $n);
if ($db->connect_errno) {
    fwrite(STDERR, "CONNECT FAIL: " . $db->connect_error . "\n");
    exit(1);
}
$db->set_charset('utf8mb4');

$r = $db->query($probe);
if ($r === false) {
    fwrite(STDERR, "SQL ERR: " . $db->error . "\n");
    exit(1);
}

$rows = array();
if ($r instanceof mysqli_result) {
    while ($x = $r->fetch_assoc()) $rows[] = $x;
}
echo json_encode($rows, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n";

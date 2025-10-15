# GUIDE DE CRÉATION DES TEMPLATES ET EXEMPLES
## Pour le TP Gestion de Projet - BTS SIO SISR

Ce document décrit le contenu attendu pour les templates et exemples de projets qui doivent être créés dans Microsoft Office / Google Workspace.

---

## 📋 TEMPLATES À CRÉER

### 1. Template_Presentation.pptx (PowerPoint)

**Description :** Template PowerPoint avec 10 slides pré-formatées pour la présentation orale

**Structure des slides :**

**Slide 1 : Page de titre**
- Titre : [Nom du projet]
- Sous-titre : Projet de gestion IT
- Champs à compléter : Noms des membres de l'équipe, Date

**Slide 2 : Contexte et enjeux**
- Titre : Contexte du projet
- Zones de texte pour : Contexte, Enjeux, Problématique

**Slide 3 : Objectifs et périmètre**
- Titre : Objectifs et périmètre
- Tableau 2 colonnes : Inclus | Exclu

**Slide 4 : Triangle QCD**
- Titre : Contraintes du projet
- Schéma triangle avec 3 sommets (Qualité, Coût, Délai)
- Zones de texte pour détailler chaque contrainte

**Slide 5 : Planning et jalons**
- Titre : Planning du projet
- Espace pour diagramme de Gantt ou timeline
- Tableau jalons avec dates

**Slide 6 : Gestion des risques**
- Titre : Top 5 des risques
- Tableau : Risque | Criticité | Stratégie | Plan d'action

**Slide 7 : Matrice RACI**
- Titre : Répartition des responsabilités
- Tableau RACI vide (5 tâches × 5 parties prenantes)

**Slide 8 : Budget prévisionnel**
- Titre : Budget
- Graphique camembert ou barres (à personnaliser)
- Tableau répartition budget par poste

**Slide 9 : Méthodologie**
- Titre : Méthodologie et outils
- Zones pour : Méthodologie choisie, Justification, Outils

**Slide 10 : Conclusion**
- Titre : Critères de succès et prochaines étapes
- Zones de texte libres

**Design :** Sobre et professionnel, couleurs bleu/gris, police Arial ou Calibri

---

### 2. Template_Planning_Gantt.xlsx (Excel)

**Description :** Fichier Excel avec diagramme de Gantt simple

**Feuille 1 : Planning**

**Colonnes :**
- A : Tâche
- B : Durée (jours)
- C : Date début
- D : Date fin
- E : Responsable
- F-AZ : Graphique Gantt (colonnes représentant les jours/semaines)

**Lignes pré-remplies (exemples) :**
1. Phase 1 - Initialisation
   - Analyse des besoins
   - Validation du cahier des charges
2. Phase 2 - Approvisionnement
   - Choix et commande matériel
   - Réception et vérification
3. Phase 3 - Installation
   - Installation infrastructure
   - Configuration réseau
4. Phase 4 - Tests
   - Tests techniques
   - Tests utilisateurs
5. Phase 5 - Déploiement
   - Formation
   - Mise en production

**Mise en forme conditionnelle :** Barres colorées dans les colonnes F-AZ pour visualiser le Gantt

**Feuille 2 : Jalons**
- Tableau : Jalon | Date prévue | Date réelle | Statut | Commentaire

---

### 3. Template_Registre_Risques.xlsx (Excel)

**Description :** Tableau Excel pour le registre des risques

**Colonnes :**
- A : ID (R01, R02, R03...)
- B : Description du risque
- C : Probabilité (Faible / Moyenne / Élevée)
- D : Impact (Faible / Moyen / Élevé)
- E : Criticité (auto-calculée : Probabilité × Impact)
- F : Stratégie de réponse (Éviter / Transférer / Atténuer / Accepter)
- G : Plan d'action détaillé
- H : Responsable du suivi
- I : Statut (Non matérialisé / En cours / Matérialisé / Clôturé)
- J : Date de mise à jour

**Lignes pré-remplies (exemples) :**
1. Retard de livraison du matériel
2. Matériel défectueux à la réception
3. Incompatibilité technique imprévue
4. Dépassement du budget
5. Absence d'un membre de l'équipe
6. Problème de connexion internet
7. Résistance au changement des utilisateurs
8. Câblage réseau non conforme

**Mise en forme conditionnelle :**
- Criticité Élevée : fond rouge
- Criticité Moyenne : fond orange
- Criticité Faible : fond vert

---

### 4. Template_Matrice_RACI.xlsx (Excel)

**Description :** Tableau Excel pour la matrice RACI

**Structure :**
- Ligne 1 : En-têtes parties prenantes (Équipe technique, Chef de projet, Direction, Utilisateurs, Fournisseur)
- Colonne A : Tâches/Livrables

**Tâches pré-remplies (exemples) :**
1. Validation du cahier des charges
2. Choix et commande du matériel
3. Installation physique des équipements
4. Configuration réseau
5. Déploiement des postes de travail
6. Tests de connectivité
7. Tests de sécurité
8. Rédaction de la documentation
9. Formation des utilisateurs
10. Recette finale du projet

**Mise en forme :**
- Cellules avec listes déroulantes : R | A | C | I | (vide)
- Validation conditionnelle : vérifier qu'il n'y a qu'un seul A par ligne

---

### 5. Template_Budget.xlsx (Excel)

**Description :** Tableau Excel pour le budget prévisionnel

**Feuille 1 : Budget détaillé**

**Colonnes :**
- A : Poste de dépense
- B : Description
- C : Quantité
- D : Prix unitaire HT
- E : Total HT (=C×D)
- F : Commentaire

**Postes pré-remplés (exemples) :**
1. Matériel réseau
   - Firewall pfSense
   - Switch 24 ports
   - Câbles et accessoires
2. Postes de travail
   - PC Dell Optiplex (×15)
3. Téléphonie VoIP
   - Serveur VoIP
   - Téléphones IP (×5)
4. Imprimantes réseau
   - Imprimantes HP (×2)
5. Licences logicielles
   - Windows Server 2022
   - Licences CAL
6. Prestations
   - Installation
   - Formation
   - Documentation
7. Marge de sécurité (5-10%)

**Ligne totale :** Budget global HT

**Feuille 2 : Graphique**
- Graphique camembert : répartition du budget par grande catégorie

---

## 📂 EXEMPLES DE PROJETS À CRÉER

### Exemple 1 : Migration Active Directory 2012 → 2022

**Dossier :** Exemple_Migration_AD/

**Fichiers à créer :**

**1. Fiche_cadrage_AD.docx**
- Contexte : Entreprise 200 postes, serveur AD 2012 en fin de support
- Objectifs : Migrer vers AD 2022, maintenir les GPO, zéro interruption
- Périmètre : Migration AD, DNS intégré, GPO, comptes utilisateurs
- Parties prenantes : DSI, équipe IT, utilisateurs, prestataire externe
- Triangle QCD : Budget 50 000 €, délai 3 mois, qualité haute
- Livrables : Nouveau serveur AD 2022, GPO migrées, documentation
- Critères de succès : Tous les postes joints au nouveau domaine, GPO fonctionnelles, 0 interruption de service

**2. Planning_AD.xlsx**
- Phase 1 : Analyse et préparation (2 semaines)
- Phase 2 : Installation nouveau serveur (1 semaine)
- Phase 3 : Migration GPO et comptes (3 semaines)
- Phase 4 : Migration des postes (4 semaines)
- Phase 5 : Tests et validation (1 semaine)
- Phase 6 : Décommissionnement ancien serveur (1 semaine)
- Jalons : J+14 (nouveau serveur OK), J+35 (migration GPO terminée), J+70 (50% des postes migrés), J+84 (validation finale)

**3. Registre_risques_AD.xlsx**
- R01 : Incompatibilité GPO avec Windows 11 (Probabilité Moyenne, Impact Élevé, Stratégie Atténuer)
- R02 : Corruption de la base NTDS lors de la migration (P Faible, I Critique, S Éviter via sauvegarde complète)
- R03 : Problème DNS lors de la bascule (P Moyenne, I Élevé, S Atténuer via tests)
- R04 : Résistance utilisateurs au changement de mot de passe (P Élevée, I Faible, S Atténuer via communication)
- R05 : Départ du consultant externe (P Faible, I Moyen, S Accepter avec plan B)

**4. Matrice_RACI_AD.xlsx**
- Exemple complet avec : Équipe IT, Chef de projet, DSI, Utilisateurs, Consultant externe

---

### Exemple 2 : Déploiement VPN pour télétravail

**Dossier :** Exemple_VPN_Teletravail/

**Fichiers à créer :**

**1. Fiche_cadrage_VPN.docx**
- Contexte : COVID-19, 100 employés doivent télétravailler en urgence
- Objectifs : VPN sécurisé opérationnel en 2 semaines
- Périmètre : VPN OpenVPN, authentification forte, formation utilisateurs
- Parties prenantes : Direction, équipe IT, utilisateurs
- Triangle QCD : Budget 20 000 €, délai 2 semaines, qualité sécurité élevée
- Livrables : Serveur VPN, clients configurés, guide utilisateur
- Critères de succès : 100% des employés peuvent se connecter au VPN, sécurité validée par audit

**2. Planning_VPN.xlsx**
- Phase 1 : Installation serveur VPN (3 jours)
- Phase 2 : Configuration et tests (4 jours)
- Phase 3 : Déploiement clients (3 jours)
- Phase 4 : Formation et support (4 jours)
- Jalons : J+3 (serveur VPN opérationnel), J+7 (tests sécurité OK), J+10 (50 clients déployés), J+14 (100% déployé)

**3. Registre_risques_VPN.xlsx**
- R01 : Incompatibilité VPN avec firewall existant
- R02 : Bande passante internet insuffisante
- R03 : Problèmes de configuration sur certains PC personnels
- R04 : Résistance utilisateurs (complexité technique perçue)
- R05 : Faille de sécurité découverte après déploiement

**4. Matrice_RACI_VPN.xlsx**
- Exemple avec : Équipe IT, Chef de projet, Direction, Utilisateurs, Fournisseur VPN

---

### Exemple 3 : Infrastructure réseau nouvelle agence

**Dossier :** Exemple_Infrastructure_Agence/

**Fichiers à créer :**

**1. Fiche_cadrage_Agence.docx**
- Contexte : Ouverture agence régionale Lyon, 15 employés
- Objectifs : Infrastructure IT complète (réseau, postes, téléphonie)
- Périmètre : Firewall, switch, 15 postes, imprimantes, téléphones VoIP, VPN site-à-site
- Parties prenantes : Direction, équipe IT, employés Lyon, fournisseurs
- Triangle QCD : Budget 35 000 €, délai 6 semaines, disponibilité 99%
- Livrables : Infrastructure opérationnelle, VPN Paris-Lyon, documentation
- Critères de succès : 15 postes opérationnels, VPN fonctionnel, formation effectuée

**2. Planning_Agence.xlsx**
- Phase 1 : Initialisation et commandes (1 semaine)
- Phase 2 : Installation infrastructure (2 semaines)
- Phase 3 : Configuration et intégration (2 semaines)
- Phase 4 : Tests et validation (1 semaine)
- Phase 5 : Formation et mise en production (1 semaine)
- Jalons : J+7 (matériel commandé), J+21 (infrastructure installée), J+35 (tests validés), J+42 (mise en production)

**3. Registre_risques_Agence.xlsx**
- R01 : Retard livraison matériel
- R02 : Câblage réseau non conforme
- R03 : Incompatibilité téléphonie VoIP avec réseau
- R04 : Problème connexion VPN Paris-Lyon
- R05 : Formation utilisateurs insuffisante

**4. Matrice_RACI_Agence.xlsx**
- Exemple avec : Équipe technique, Chef de projet, Direction, Employés Lyon, Fournisseurs

---

## 📝 INSTRUCTIONS DE CRÉATION

### Pour les templates Excel :
1. Créer le fichier avec la structure décrite
2. Ajouter des exemples de données pour illustrer l'utilisation
3. Appliquer une mise en forme professionnelle (couleurs sobres, bordures)
4. Ajouter des formules automatiques où pertinent (calcul criticité, total budget)
5. Protéger les cellules de formule pour éviter les erreurs

### Pour le template PowerPoint :
1. Utiliser un design sobre (thème Office ou personnalisé)
2. Police : Arial ou Calibri, taille 20-24 pour le texte, 32-36 pour les titres
3. Couleurs : bleu (#0066CC), gris (#666666), blanc (#FFFFFF)
4. Inclure des zones de texte pré-formatées et des placeholders pour images
5. Ajouter des notes de présentation avec conseils dans chaque slide

### Pour les exemples de projets :
1. Créer un dossier par projet
2. Tous les fichiers doivent être cohérents entre eux (mêmes dates, budget, parties prenantes)
3. Utiliser des données réalistes basées sur des projets IT réels
4. Ajouter des commentaires pour expliquer les choix faits

---

## 💾 ORGANISATION DES FICHIERS SUR MOODLE

```
Ressources TP Gestion de Projet/
├── Templates/
│   ├── Template_Presentation.pptx
│   ├── Template_Planning_Gantt.xlsx
│   ├── Template_Registre_Risques.xlsx
│   ├── Template_Matrice_RACI.xlsx
│   └── Template_Budget.xlsx
├── Exemples_Projets/
│   ├── Exemple_Migration_AD/
│   │   ├── Fiche_cadrage_AD.docx
│   │   ├── Planning_AD.xlsx
│   │   ├── Registre_risques_AD.xlsx
│   │   └── Matrice_RACI_AD.xlsx
│   ├── Exemple_VPN_Teletravail/
│   │   ├── Fiche_cadrage_VPN.docx
│   │   ├── Planning_VPN.xlsx
│   │   ├── Registre_risques_VPN.xlsx
│   │   └── Matrice_RACI_VPN.xlsx
│   └── Exemple_Infrastructure_Agence/
│       ├── Fiche_cadrage_Agence.docx
│       ├── Planning_Agence.xlsx
│       ├── Registre_risques_Agence.xlsx
│       └── Matrice_RACI_Agence.xlsx
└── Guides/
    ├── Guide_Triangle_QCD.html (fourni)
    ├── Guide_Gestion_Risques.html (fourni)
    └── Guide_Matrice_RACI.html (fourni)
```

---

**Note :** Ces templates et exemples sont à créer dans Microsoft Office ou Google Workspace puis à télécharger sur Moodle dans la section du TP Gestion de Projet.

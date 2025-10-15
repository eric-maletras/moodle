# 🧩 Projet VPN Télétravail M2L  
**Équipe BTS SIO – Projet VPN Télétravail M2L**  

## 📘 Contexte du projet
Suite à la crise sanitaire (COVID-19), 100 employés de la M2L doivent pouvoir télétravailler en urgence.  
L’objectif est de déployer une **solution VPN OpenVPN** sécurisée, opérationnelle sous **2 semaines**, garantissant un accès distant fiable et conforme aux bonnes pratiques de cybersécurité.

---

## 🎯 Objectifs
- Mettre en place un **VPN sécurisé et fonctionnel** dans un délai de 14 jours.  
- Garantir la **confidentialité**, l’**intégrité** et la **disponibilité** des connexions distantes.  
- Former les utilisateurs à l’usage du VPN et à la sécurité des accès.

---

## 📦 Livrables
- Serveur OpenVPN installé et configuré.  
- 100 clients VPN configurés et testés.  
- Guide utilisateur et documentation technique.  
- Validation sécurité par audit interne.

---

## ⚙️ Détails du dossier

| Fichier | Type | Description |
|----------|------|-------------|
| 🧾 **[Fiche_cadrage_VPN.docx](./Fiche_cadrage_VPN.docx)** | Word | Fiche simplifiée présentant le contexte, les objectifs, le périmètre et les critères de succès. |
| 📅 **[Planning_VPN.xlsx](./Planning_VPN.xlsx)** | Excel | Planning prévisionnel sur 2 semaines (phases, jalons et durée totale). |
| ⚠️ **[Registre_risques_VPN.xlsx](./Registre_risques_VPN.xlsx)** | Excel | Registre des 5 risques principaux, avec criticité calculée et plans d’action. |
| 🧩 **[Matrice_RACI_VPN.xlsx](./Matrice_RACI_VPN.xlsx)** | Excel | Répartition des rôles et responsabilités (RACI) : Équipe IT, Chef de projet, Direction, Utilisateurs, Fournisseur VPN. |

---

## 📅 Planning global
| Phase | Durée | Jalons |
|--------|--------|---------|
| Installation serveur VPN | 3 jours | **J+3** : Serveur opérationnel |
| Configuration et tests | 4 jours | **J+7** : Tests sécurité OK |
| Déploiement clients | 3 jours | **J+10** : 50 clients déployés |
| Formation et support | 4 jours | **J+14** : 100% déployé |

📆 **Date de début : 16/10/2025**  
📆 **Date de fin prévue : 29/10/2025**

---

## ⚠️ Risques principaux

| ID | Risque | Probabilité | Impact | Criticité |
|----|---------|-------------|---------|------------|
| R01 | Incompatibilité VPN avec firewall existant | Moyenne | Élevé | Élevée |
| R02 | Bande passante internet insuffisante | Élevée | Élevé | Élevée |
| R03 | Problèmes de configuration sur certains PC personnels | Moyenne | Moyen | Moyenne |
| R04 | Résistance utilisateurs (complexité perçue) | Faible | Moyen | Faible |
| R05 | Faille de sécurité découverte après déploiement | Faible | Élevé | Moyenne |

---

## 👥 Matrice RACI (extrait)

| Tâche | Équipe IT | Chef de projet | Direction | Utilisateurs | Fournisseur VPN |
|--------|------------|----------------|------------|---------------|----------------|
| Installation serveur VPN | **R** | **A** |  |  |  |
| Tests sécurité | **R** | **A** | **C** |  |  |
| Déploiement clients | **R** | **A** |  | **I** | **C** |
| Formation utilisateurs | **C** | **A** |  | **R** |  |
| Audit de sécurité final | **R** | **A** | **C** |  | **I** |

---

## ✅ Critères de succès
- 100 % des employés peuvent se connecter au VPN.  
- Aucun incident majeur de sécurité signalé.  
- Tests d’audit validés par l’équipe cybersécurité.  
- Satisfaction utilisateurs > 90 % lors du retour post-déploiement.

---

## 🧠 Bonnes pratiques recommandées
- Utiliser **authentification forte** (certificats et mots de passe robustes).  
- Vérifier régulièrement les **logs OpenVPN** pour détecter les connexions suspectes.  
- Documenter la **procédure d’urgence** en cas de faille ou d’indisponibilité du VPN.  
- Mettre à jour le serveur et les clients OpenVPN régulièrement.

---

## © Auteurs
**Équipe BTS SIO – Projet VPN Télétravail M2L**  
Encadrement : Formateur SISR / Chef de projet IT  
Date : Octobre 2025  
Version : 1.0


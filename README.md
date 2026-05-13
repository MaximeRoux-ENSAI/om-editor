# om-editor

Application Python permettant de générer facilement des ordres de mission administratifs à partir de modèles Word.

Pensée initialement pour les élèves de l’ENSAI, l’application vise à simplifier la création et le remplissage des formulaires d’ordre de mission pour différents types de déplacements : stages, formations, conférences, représentation de l’école, missions professionnelles, etc.

Le projet repose sur une architecture simple et extensible basée sur Python, Streamlit et des modèles `.docx`.

---

# État du projet

Le projet est déjà fonctionnel pour une grande partie des usages courants.

Actuellement, `om-editor` permet de générer automatiquement le **corps principal d’un ordre de mission** pour les cas les plus fréquents :

- stages ;
- représentations d’école ;
- forums / salons ;
- formations ;
- conférences ;
- déplacements administratifs classiques.

Les cas pris en charge incluent :

- trajets en train ;
- trajets avec carte d’abonnement SNCF ;
- trajets en voiture ;
- profils agent / élève ;
- trajets multi-étapes ;
- périodes de convenances personnelles.

Certaines parties spécifiques des OM restent encore à compléter manuellement selon les besoins :

- réservation d’hôtel ;
- repas ;
- avion ;
- frais particuliers ;
- informations CREST / laboratoire ;
- validations administratives spécifiques.

L’objectif du projet est donc :
> automatiser la partie pénible, répétitive et chronophage des ordres de mission, tout en conservant la possibilité de compléter manuellement les cas particuliers.

---

# Fonctionnalités

- Génération automatique d’ordres de mission `.docx`
- Profils missionnaires sauvegardés
- Types de mission préconfigurés
- Préremplissage des informations récurrentes
- Gestion des trajets multi-étapes
- Support train / abonnement SNCF / voiture
- Templates distincts agent / élève
- Interface Streamlit légère et simple d’utilisation

---

# Technologies utilisées

- Python
- Streamlit
- docxtpl
- python-docx
- PyYAML
- uv

---

# Installation

## 1. Cloner le dépôt

```bash
git clone https://github.com/<votre-utilisateur>/om-editor.git
cd om-editor
```

## 2. Installer les dépendances

Le projet utilise `uv` pour la gestion des dépendances.

```bash
uv sync
```

---

# Lancement

```bash
uv run streamlit run app.py
```

---

# Structure du projet

```text
om-editor/
├── app.py
├── pyproject.toml
├── templates/
├── generated/
├── data/
├── src/
└── tests/
```

---

# Configuration des profils

Le dossier `data/` est ignoré par Git afin de permettre à chaque utilisateur de conserver ses propres profils locaux.

Créer un fichier :

```text
data/profils.yaml
```

Exemple :

```yaml
default:
  nom: DUPONT
  prenom: Jean
  date_naissance: "2000-01-01"
  mail: jean.dupont@example.com
  telephone: ""
  adresse: ""
  code_postal: "00000"
  ville: Paris
  nationalite: Française
  profession: Étudiant
```

Ces profils permettent de préremplir automatiquement les informations du missionnaire.

---

# Configuration des types de mission

Créer un fichier :

```text
data/mission_types.yaml
```

Exemple :

```yaml
aucun:
  label: Aucun préremplissage
  motif: ""

stage:
  label: Stage
  motif: "Stage à préciser"

representation_ensai:
  label: Représentation ENSAI
  motif: "Représentation de l’ENSAI lors d’un événement extérieur"

formation:
  label: Formation
  motif: "Participation à une formation"

conference:
  label: Conférence
  motif: "Participation à une conférence"
```

---

# Génération des documents

Les documents générés sont enregistrés dans :

```text
generated/
```

Le dossier est ignoré par Git afin d’éviter de versionner des documents générés automatiquement.

---

# Roadmap

Fonctionnalités envisagées :

- Export PDF
- Validation automatique des champs
- Historique des missions
- Déploiement web léger
- Support complet des missions avion
- Génération automatique des réservations
- Remplissage avancé des frais et nuitées

---

# Licence

Projet distribué sous licence GNU GPL v3.

Toute version modifiée ou redistribuée du projet doit également rester open source sous la même licence.
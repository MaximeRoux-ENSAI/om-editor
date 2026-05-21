# 🧳 om-editor

Application Python permettant de générer facilement des ordres de mission administratifs à partir de modèles Word.

Pensée initialement pour les élèves de l’ENSAI, l’application vise à simplifier la création et le remplissage des formulaires d’ordre de mission pour différents types de déplacements : stages, formations, conférences, représentation de l’école, missions professionnelles, etc.

Le projet repose sur une architecture simple et extensible basée sur Python, Streamlit et des modèles `.docx`.

---

# 📚 Sommaire

- [🚧 État du projet](#-état-du-projet)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🛠️ Technologies utilisées](#️-technologies-utilisées)
- [⚙️ Installation](#️-installation)
- [▶️ Lancement](#️-lancement)
- [🐳 Utilisation avec Docker](#-utilisation-avec-docker)
- [📁 Structure du projet](#-structure-du-projet)
- [👤 Configuration des profils](#-configuration-des-profils)
- [🧾 Configuration des types de mission](#-configuration-des-types-de-mission)
- [📄 Génération des documents](#-génération-des-documents)
- [🗺️ Roadmap](#️-roadmap)
- [❓ FAQ](#-faq)
- [👨‍💻 Auteur](#-auteur)
- [📜 Licence](#-licence)

---

# 🚧 État du projet

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
- trajets train + avion ;
- trajets en voiture ;
- hébergement ;
- nuitées ;
- repas prévisionnels ;
- profils agent / élève ;
- trajets multi-étapes ;
- périodes de convenances personnelles.

L’application permet également :

- la sélection automatique du template adapté ;
- le préremplissage via profils utilisateurs ;
- la validation automatique de certains champs ;
- la gestion de plusieurs workflows administratifs selon le mode de transport.

Certaines parties spécifiques des OM restent encore à compléter manuellement selon les besoins :

- validations administratives internes ;
- frais très spécifiques ;
- cas exceptionnels liés aux missions internationales ;
- intégration poussée avec les outils administratifs du GENES / INSEE.

L’objectif du projet est donc :

> automatiser la partie pénible, répétitive et chronophage des ordres de mission, tout en conservant la possibilité de compléter manuellement les cas particuliers.

---

# ✨ Fonctionnalités

- Génération automatique d’ordres de mission `.docx`
- Profils missionnaires sauvegardés
- Types de mission préconfigurés
- Préremplissage des informations récurrentes
- Gestion des trajets multi-étapes
- Support train / abonnement SNCF / train + avion / voiture
- Gestion des hébergements et nuitées
- Gestion des repas prévisionnels
- Templates distincts agent / élève
- Validation automatique de certains champs
- Interface Streamlit légère et simple d’utilisation

---

# 🛠️ Technologies utilisées

- Python
- Streamlit
- docxtpl
- python-docx
- PyYAML
- uv

---

# ⚙️ Installation

## 1. Cloner le dépôt

```bash
git clone https://github.com/MaximeRoux-ENSAI/om-editor.git
cd om-editor
```

## 2. Installer les dépendances

Le projet utilise `uv` pour la gestion des dépendances.

```bash
uv sync
```

---

# ▶️ Lancement

```bash
uv run streamlit run app.py
```

---

# 🐳 Utilisation avec Docker

L’application peut être exécutée dans un conteneur Docker, ce qui facilite le déploiement sur des plateformes comme Onyxia / SSPCloud.

## 1. Construire l’image Docker

Depuis la racine du projet :

```bash
docker build -t om-editor .
```

## 2. Lancer le conteneur

```bash
docker run -p 8501:8501 om-editor
```

L’application sera alors accessible à l’adresse :

```text
http://localhost:8501
```

## 3. Arrêter le conteneur

Dans le terminal courant :

```text
CTRL + C
```

Ou, si le conteneur tourne en arrière-plan :

```bash
docker ps
docker stop <container_id>
```

## 4. Fichiers Docker attendus

Le projet utilise :

```text
Dockerfile
.dockerignore
```

afin de permettre un déploiement simple et reproductible.

# 📁 Structure du projet

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

# 👤 Configuration des profils

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

# 🧾 Configuration des types de mission

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

# 📄 Génération des documents

Les documents générés sont enregistrés dans :

```text
generated/
```

Le dossier est ignoré par Git afin d’éviter de versionner des documents générés automatiquement.

---

# 🗺️ Roadmap

Fonctionnalités envisagées :

- Export PDF
- Déploiement web léger
- Intégration plus poussée des frais administratifs
- Support avancé des missions internationales

---

# ❓ FAQ

## Pourquoi faut-il parfois appuyer sur “Entrée” après avoir changé le nombre de trajets ?

L’application utilise actuellement les formulaires Streamlit (`st.form`) afin de conserver une interface cohérente et éviter des rechargements permanents de la page.

À cause de cette limitation technique de Streamlit, lorsque vous utilisez les boutons `+` ou `-` pour modifier :
- le nombre de trajets ;
- le nombre de convenances personnelles ;
- ou certaines valeurs numériques,

il peut être nécessaire d’appuyer sur `Entrée` pour valider immédiatement le changement.

Cela n’impacte pas la génération finale du document, mais uniquement l’actualisation visuelle du formulaire.

Une amélioration ergonomique sur ce point pourra être étudiée dans une future version.

---

## Quels logiciels permettent d’ouvrir les documents générés ?

Les documents générés sont au format `.docx`.

Ils peuvent être ouverts avec :
- Microsoft Word ;
- LibreOffice Writer ;
- OnlyOffice ;
- Google Docs (avec quelques différences possibles de mise en page).

Le rendu recommandé reste Microsoft Word ou LibreOffice.

---

## Est-ce que tous les types d’ordres de mission sont pris en charge ?

Non.

L’application couvre principalement les cas “classiques” rencontrés à l’ENSAI / GENES :
- train ;
- voiture ;
- hébergement simple ;
- abonnement SNCF ;
- train + avion.

Certains cas très spécifiques ou administrativement complexes peuvent encore nécessiter des modifications manuelles.

---

## Mes données personnelles sont-elles envoyées quelque part ?

Non.

L’application fonctionne localement et ne transmet aucune donnée à un serveur externe.

Les profils utilisateurs sont stockés localement dans le dossier `data/`, qui est ignoré par Git.

---

## Puis-je modifier les templates Word ?

Oui.

Les modèles `.docx` présents dans le dossier `templates/` peuvent être adaptés ou personnalisés selon les besoins de votre établissement ou service.

---

## Pourquoi l’application génère-t-elle du `.docx` plutôt que du PDF ?

Le format `.docx` permet :
- de conserver un document facilement modifiable ;
- de garantir une meilleure compatibilité avec les modèles administratifs existants ;
- et d’éviter des dépendances lourdes liées à la conversion PDF.

L’utilisateur peut ensuite exporter lui-même le document en PDF si nécessaire.

---

## Puis-je contribuer au projet ?

Oui !

Les issues, suggestions, améliorations ergonomiques et pull requests sont les bienvenues.

---

# 👨‍💻 Auteur

- Maxime ROUX  
  GitHub : https://github.com/MaximeRoux-ENSAI

---

# 📜 Licence

Projet distribué sous licence GNU GPL v3.

Toute version modifiée ou redistribuée du projet doit également rester open source sous la même licence.
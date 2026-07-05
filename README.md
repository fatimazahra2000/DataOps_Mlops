# 🎬 MovieLens Recommendation System — MLOps & DataOps Project

## 📖 Description

Ce projet a été réalisé dans le cadre du module **MLOps & DataOps**.

L'objectif est de construire un **pipeline DataOps/MLOps complet** permettant de générer des recommandations personnalisées de films à partir du dataset **MovieLens**.

Le projet couvre tout le cycle de vie d'un produit IA :

- 📥 Ingestion automatisée des données (dlt)
- 🗄️ Stockage local (DuckDB)
- 🔄 Transformation des données (dbt)
- ✅ Contrôle qualité & Data Contracts
- 🎯 Préparation Machine Learning
- 🤖 Entraînement du modèle de recommandation
- 📊 Tracking des expériences (MLflow)
- 🚀 Déploiement avec FastAPI
- 🐳 Conteneurisation
- ⚙️ CI/CD
- 📈 Monitoring

---

# 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Data Ingestion | dlt |
| Database | DuckDB |
| Data Transformation | dbt |
| Data Quality | dbt Tests + Python |
| Orchestration | Dagster |
| Machine Learning | Scikit-Learn |
| Experiment Tracking | MLflow *(à venir)* |
| API | FastAPI *(à venir)* |
| CI/CD | GitHub Actions *(à venir)* |
| Containerisation | Docker *(à venir)* |

---

# 👥 Équipe

| Membre | Responsabilité |
|---------|----------------|
| Zainab | Vision du projet + Dagster |
| Fatima | Gestion Agile + GitHub |
| Douaa | Ingestion des données |
| Hasena | DuckDB & dbt |
| Hajar | Qualité des données |
| Yousera | Préparation Machine Learning |
| Jihad | Modèle de recommandation |
| Hafesa | MLflow & Monitoring |
| Amina | FastAPI, Docker, CI/CD |

---

# 🌿 Organisation Git

Le projet suit la stratégie Git suivante :

| Branche | Utilisation |
|----------|-------------|
| `main` | Version stable du projet |
| `develop` | Branche principale de développement |
| `feature/model` | Développement du modèle ML (Jihad) |
| `feature/mlflow` | Intégration MLflow (Hafesa) |
| `feature/api` | API, Docker et CI/CD (Amina) |

⚠️ **Aucun développement ne doit être effectué directement sur `main`.**

Toutes les nouvelles fonctionnalités doivent être développées sur leur branche dédiée puis fusionnées dans `develop` via une **Pull Request**.

---

# 🤝 Collaboration Git

## 1. Cloner le projet

```bash
git clone https://github.com/fatimazahra2000/DataOps_Mlops.git
cd DataOps_Mlops
```

---

## 2. Installer les dépendances

Créer un environnement virtuel.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## 3. Configurer les variables d'environnement

Copier le fichier :

```bash
cp .env.example .env
```

Sous Windows :

```powershell
copy .env.example .env
```

---

## 4. Accéder à la branche de développement

Avant de commencer à travailler :

```bash
git checkout develop
git pull origin develop
```

---

## 5. Se placer sur sa branche

### Jihad

```bash
git checkout feature/model
```

### Hafesa

```bash
git checkout feature/mlflow
```

### Amina

```bash
git checkout feature/api
```

---

## 6. Vérifier la branche courante

```bash
git branch
```

La branche active est précédée d'un `*`.

Exemple :

```text
* feature/model
  develop
  main
```

---

## 7. Sauvegarder son travail

```bash
git add .
git commit -m "Description des modifications"
git push
```

---

## 8. Mettre sa branche à jour

Lorsque de nouvelles modifications ont été intégrées dans `develop` :

```bash
git checkout develop
git pull origin develop
```

Puis revenir sur sa branche :

### Jihad

```bash
git checkout feature/model
git merge develop
```

### Hafesa

```bash
git checkout feature/mlflow
git merge develop
```

### Amina

```bash
git checkout feature/api
git merge develop
```

---

## 9. Fin du développement

Lorsque la fonctionnalité est terminée :

- pousser les dernières modifications :

```bash
git push
```

- créer une **Pull Request** de votre branche vers `develop` ;
- attendre la validation avant la fusion.

⚠️ Ne jamais pousser directement sur `main`.

---

# ⚙️ Installation du projet

Après installation des dépendances :

### Ingestion des données

```bash
python ingestion.py
```

---

### Vérification de la base DuckDB

```bash
python check_db.py
```

---

### Transformation des données

```bash
cd transform_data

dbt run

dbt test

cd ..
```

---

### Contrôle qualité

```bash
python data_quality_check.py
```

---

### Lancer Dagster

```bash
dagster dev -m orchestration.definitions
```
---

# 📌 État actuel du projet

Légende :

- ✅ Terminé
- ⏳ À réaliser

---

## 📚 Documentation (`docs/`)

| Élément | Statut | Responsable |
|----------|--------|-------------|
| `vision_projet.md` | ✅ | Zainab |
| `product_backlog.md` | ✅ | Fatima |
| `sprints.md` | ✅ | Fatima |
| `data_lineage.md` | ✅ | Hajar |
| `architecture.md` | ⏳ | À créer |
| `guide_installation.md` | ⏳ | À créer |

---

## 📥 Ingestion des données

| Élément | Statut | Responsable |
|----------|--------|-------------|
| `ingestion.py` | ✅ | Douaa |
| `check_db.py` | ✅ | Douaa |
| Dataset MovieLens | ✅ | Douaa |

L'ingestion est réalisée avec **dlt** et les données sont automatiquement chargées dans **DuckDB**.

---

## 🔄 Transformation des données (dbt)

| Élément | Statut | Responsable |
|----------|--------|-------------|
| `dbt_project.yml` | ✅ | Hasena |
| `profiles.yml` | ✅ | Hasena |
| `sources.yml` | ✅ | Hajar |
| `schema.yml` | ✅ | Hajar |
| `recommandation_prete.sql` | ✅ | Hasena |
| Tests SQL personnalisés | ✅ | Hajar |

La table finale utilisée par le modèle est :

```
recommandation_prete
```

Elle contient notamment :

- user_id
- movie_id
- title
- genres
- rating

---

## ✅ Qualité des données

| Élément | Statut | Responsable |
|----------|--------|-------------|
| `data_quality_check.py` | ✅ | Hajar |
| Data Contracts | ✅ | Hajar |
| Data Lineage | ✅ | Hajar |

Les contrôles portent sur :

- valeurs manquantes
- doublons
- types
- plage des notes
- cohérence des relations

---

## ⚙️ Orchestration

| Élément | Statut | Responsable |
|----------|--------|-------------|
| `assets.py` | ✅ | Zainab |
| `definitions.py` | ✅ | Zainab |

Dagster orchestre automatiquement :

- ingestion
- dbt run
- dbt test
- contrôle qualité
- préparation du dataset

---

## 🤖 Machine Learning

| Élément | Statut | Responsable |
|----------|--------|-------------|
| `prepare_data.ipynb` | ✅ | Yousera |
| `feature_engineering.ipynb` | ✅ | Yousera |
| `preprocessing.ipynb` | ✅ | Yousera |
| `processed/` | ✅ | Yousera |
| `train.py` | ⏳ | Jihad |
| `evaluate.py` | ⏳ | Jihad |
| `models/model.pkl` | ⏳ | Jihad |

---

## 📊 MLflow

| Élément | Statut | Responsable |
|----------|--------|-------------|
| `mlflow_utils.py` | ⏳ | Hafesa |
| Documentation MLflow | ⏳ | Hafesa |

---

## 🚀 API

| Élément | Statut | Responsable |
|----------|--------|-------------|
| `main.py` | ⏳ | Amina |
| `requirements_api.txt` | ⏳ | Amina |

L'API devra fournir :

```
POST /predict
GET /health
```

---

## 📈 Monitoring

| Élément | Statut | Responsable |
|----------|--------|-------------|
| Documentation Monitoring | ⏳ | Amina & Hafesa |

---

## ⚙️ CI/CD

| Élément | Statut | Responsable |
|----------|--------|-------------|
| GitHub Actions | ⏳ | Amina |

---

# 🔁 Pipeline DataOps

```text
MovieLens Dataset
        │
        ▼
dlt
        │
        ▼
DuckDB
        │
        ▼
dbt
        │
        ▼
Tests dbt
        │
        ▼
Contrôle Qualité
        │
        ▼
Préparation Machine Learning
        │
        ▼
Modèle de recommandation
        │
        ▼
MLflow
        │
        ▼
FastAPI
        │
        ▼
Monitoring
```

L'ensemble de cette chaîne est automatisé grâce à **Dagster**.

---

# 👤 Travail restant par membre

## Jihad

Développer :

- `ML/train.py`
- `ML/evaluate.py`
- `ML/models/model.pkl`

---

## Hafesa

Développer :

- `mlflow_tracking/mlflow_utils.py`
- `README_mlflow.md`

Participer également au monitoring.

---

## Amina

Développer :

- `api/main.py`
- `requirements_api.txt`
- `GitHub Actions`
- Docker
- Monitoring

---

## Non attribué

Créer :

- `docs/architecture.md`
- `docs/guide_installation.md`

---

# 📂 Structure actuelle du projet

```text
DataOps_Mlops/
│
├── .github/
│   └── workflows/
│
├── api/
│
├── data/
│
├── docs/
│
├── ML/
│
├── mlflow_tracking/
│
├── monitoring/
│
├── orchestration/
│
├── transform_data/
│
├── .env.example
├── .gitignore
├── check_db.py
├── data_quality_check.py
├── ingestion.py
├── README.md
└── requirements.txt
```

---

# 📌 Variables d'environnement

Le projet utilise le fichier :

```
.env
```

à partir du modèle :

```
.env.example
```

Variables actuellement utilisées :

```
DATA_DIR=data

DUCKDB_PATH=movielens_pipeline.duckdb

MLFLOW_TRACKING_URI=file:./mlruns

API_PORT=8000
```

---

# 📝 Bonnes pratiques

✔️ Toujours travailler sur sa branche.

✔️ Faire des commits réguliers.

✔️ Écrire un message de commit clair.

✔️ Tester son code avant de pousser.

✔️ Ouvrir une Pull Request vers `develop`.

✔️ Attendre la validation avant fusion.

❌ Ne jamais travailler directement sur `main`.

❌ Ne jamais supprimer le travail d'un autre membre.

❌ Ne jamais modifier les fichiers hors de sa responsabilité sans concertation.

---

# 📜 Licence

Projet académique réalisé dans le cadre du module **MLOps & DataOps**.
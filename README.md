# 🎬 Système de recommandation de films — Projet MLOps MovieLens

Ce projet a pour objectif de construire un **pipeline MLOps complet**, de l'ingestion des données brutes jusqu'au déploiement d'une API de recommandation de films, en s'appuyant sur le jeu de données **MovieLens**.

Le pipeline couvre : l'ingestion des données, leur transformation/qualité, l'orchestration, l'entraînement du modèle de Machine Learning, le tracking des expériences, l'exposition via une API, et la mise en conteneur (Docker) avec CI/CD.

---

## 📌 État actuel du projet

Légende : ✅ Fait · ⏳ À faire

### 1. Documentation (`docs/`)
| Fichier | Statut | Responsable |
|---|---|---|
| `docs/vision_projet.md` | ✅ Fait | **Zainab** |
| `docs/product_backlog.md` | ✅ Fait | **Fatima** |
| `docs/sprints.md` | ✅ Fait | **Fatima** |
| `docs/data_lineage.md` | ✅ Fait | **Hajar** |
| `docs/architecture.md` | ❌ — à créer | — |
| `docs/guide_installation.md` | ⏳ À faire | — |

### 2. Ingestion des données
| Fichier | Statut | Responsable | Détail |
|---|---|---|---|
| `ingestion.py` | ✅ Fait | **Douaa** | Charge `movies.csv`, `ratings.csv`, `tags.csv`, `links.csv` et les envoie dans DuckDB via `dlt`. Chemin des données configurable via la variable d'environnement `DATA_DIR`. |
| `check_db.py` | ✅ Fait | **Douaa** | Vérifie le contenu de la base DuckDB. Chemin de la DB configurable via variable d'environnement. |
| `data/` (movies, ratings, tags, links, README.txt) | ✅ Fait | — | Données sources MovieLens. |

### 3. Transformation des données (dbt)
| Élément | Statut | Responsable |
|---|---|---|
| `transform_data/dbt_project.yml`, `profiles.yml` | ✅ Fait | **Hasena + Hajar** |
| `transform_data/models/sources.yml` | ✅ Fait | Définit les sources brutes (`movies`, `ratings`, `links`) avec tests dbt (`unique`, `not_null`, `relationships`). |
| `transform_data/models/recommandation_prete.sql` | ✅ Fait | Jointure `ratings` + `movies` → table finale `recommandation_prete` (user_id, movie_id, title, rating, genres). |
| `transform_data/tests/*.sql` | ✅ Fait | Tests personnalisés : pas de doublons (user_id, movie_id), rating dans la bonne plage. |

### 4. Qualité des données
| Fichier | Statut | Responsable |
|---|---|---|
| `data_quality_check.py` | ✅ Fait | **Hajar** — Vérifie valeurs manquantes, doublons, ratings hors plage. Chemin DB via variable d'environnement. |

### 5. Orchestration (Dagster)
| Fichier | Statut | Responsable |
|---|---|---|
| `orchestration/assets.py` | ✅ Fait | Enchaîne : ingestion → dbt run → dbt test → contrôle qualité → dataset prêt pour le ML. |
| `orchestration/definitions.py` | ✅ Fait | Déclare le job Dagster `pipeline_dataops_complet` regroupant tous les assets. |

### 6. Machine Learning (`ML/`)
| Fichier | Statut | Responsable |
|---|---|---|
| `ML/prepare_data.ipynb` | ✅ Fait | **Yousera** |
| `ML/feature_engineering.ipynb` | ✅ Fait | **Yousera** |
| `ML/preprocessing.ipynb` | ✅ Fait | **Yousera** |
| `ML/processed/*.csv` | ✅ Fait | Jeux de données train/test générés. |
| `ML/train.py` | ⏳ À faire | **Jihad** |
| `ML/evaluate.py` | ⏳ À faire | **Jihad** |
| `ML/models/model.pkl` | ⏳ À faire | **Jihad** |

### 7. Suivi des expériences (MLflow)
| Fichier | Statut | Responsable |
|---|---|---|
| `mlflow_tracking/mlflow_utils.py` | ⏳ À faire | **Hafesa** — devra utiliser `MLFLOW_TRACKING_URI` en variable d'environnement (déjà prévue dans `.env.example`). |
| `mlflow_tracking/README_mlflow.md` | ⏳ À faire | **Hafesa** |

### 8. API
| Fichier | Statut | Responsable |
|---|---|---|
| `api/main.py` | ⏳ À faire | **Amina** — l'API devra écouter sur `0.0.0.0` (pour fonctionner dans Docker). |
| `api/requirements_api.txt` | ⏳ À faire | **Amina** |

### 9. Monitoring
| Fichier | Statut | Responsable |
|---|---|---|
| `monitoring/monitoring_notes.md` | ⏳ À faire | **Amina / Hafesa** |

### 10. Conteneurisation & CI/CD
| Fichier | Statut | Responsable |
|---|---|---|
| `docker/docker-compose.yml` | ⏳ À faire | **Amina** — Doit assembler FastAPI + MLflow + Dagster en une seule stack. |
| `docker/api.Dockerfile` | ⏳ À faire | **Amina** |
| `docker/mlflow.Dockerfile` | ⏳ À faire | **Amina** |
| `docker/dagster.Dockerfile` | ⏳ À faire | **Amina** |
| `.github/workflows/ci.yml` | ⏳ À faire | **Amina** |

### 11. Configuration
| Fichier | Statut | Détail |
|---|---|---|
| `.env.example` | ✅ Fait | Modèle des variables d'environnement : `DATA_DIR`, `DUCKDB_PATH`, `MLFLOW_TRACKING_URI`, `API_PORT`. |
| `requirements.txt` | ✅ Fait | Dépendances actuelles : `dlt`, `duckdb`, `pandas`, `pyarrow`, `dbt-core`, `dbt-duckdb`, `scikit-learn`, `jupyter`, `dagster`, `dagster-webserver`. |
| `.gitignore` | ✅ Fait | — |

---

## 🔁 Pipeline de données (résumé du data lineage)

```
data/*.csv (movies, ratings, tags, links)
      │
      ▼
ingestion.py (dlt)  ──────────────► DuckDB (schéma raw_data)
      │
      ▼
dbt run (transform_data/models/recommandation_prete.sql)
      │  jointure ratings + movies
      ▼
table finale : recommandation_prete   (Data Contract respecté via dbt tests)
      │
      ▼
data_quality_check.py  (valeurs manquantes, doublons, ratings hors plage)
      │
      ▼
ML/prepare_data.ipynb → feature_engineering.ipynb → preprocessing.ipynb
      │
      ▼
ML/train.py  ⏳  →  MLflow tracking ⏳  →  model.pkl ⏳
      │
      ▼
api/main.py ⏳  (expose le modèle via FastAPI)
      │
      ▼
docker-compose (FastAPI + MLflow + Dagster) ⏳  +  CI/CD (GitHub Actions) ⏳
```

Toute cette chaîne est automatisée par **Dagster** (`orchestration/assets.py` et `definitions.py`), qui exécute dans l'ordre : ingestion → dbt run → dbt test → contrôle qualité → dataset prêt pour le ML.

---

## 👥 Ce qu'il reste à faire, par personne

### Amina
- `docker/docker-compose.yml` + les 3 Dockerfiles (`api`, `mlflow`, `dagster`)
- `.github/workflows/ci.yml` (pipeline CI/CD)
- `api/main.py` et `api/requirements_api.txt` (API FastAPI, écoute sur `0.0.0.0`)
- `monitoring/monitoring_notes.md` (avec Hafesa)

### Jihad
- `ML/train.py` : script d'entraînement du modèle de recommandation
- `ML/evaluate.py` : script d'évaluation du modèle
- `ML/models/model.pkl` : modèle entraîné sauvegardé

### Hafesa
- `mlflow_tracking/mlflow_utils.py` : utilitaires de tracking MLflow (utiliser la variable d'environnement `MLFLOW_TRACKING_URI`)
- `mlflow_tracking/README_mlflow.md` : documentation MLflow
- `monitoring/monitoring_notes.md` (avec Amina)

### Reste à faire / non attribué
- `docs/guide_installation.md` : guide d'installation du projet
- `docs/architecture.md` : **à retrouver ou reconstruire**

---

## ⚙️ Installation rapide (en l'état actuel)

```bash
# 1. Cloner le dépôt et se placer dans le dossier
cd projet_mlops_movielens

# 2. Créer un environnement virtuel et installer les dépendances
python -m venv venv
source venv/bin/activate      # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt

# 3. Copier le fichier d'environnement
cp .env.example .env

# 4. Lancer l'ingestion des données
python ingestion.py

# 5. Vérifier la base DuckDB
python check_db.py

# 6. Lancer les transformations dbt
cd transform_data
dbt run
dbt test
cd ..

# 7. Vérifier la qualité des données
python data_quality_check.py

# 8. Lancer le pipeline complet via Dagster
dagster dev -m orchestration.definitions
```

*(Un guide d'installation détaillé sera fourni dans `docs/guide_installation.md`, à rédiger.)*

---

## 📂 Structure cible du projet

```
projet_mlops_movielens/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── .github/workflows/ci.yml                 ⏳ Amina
├── docker/                                  ⏳ Amina
│   ├── docker-compose.yml
│   ├── api.Dockerfile
│   ├── mlflow.Dockerfile
│   └── dagster.Dockerfile
├── docs/
│   ├── vision_projet.md                     ✅ Zainab
│   ├── product_backlog.md                   ✅ Fatima
│   ├── sprints.md                           ✅ Fatima
│   ├── data_lineage.md                      ✅ Hajar
│   ├── architecture.md                      ⏳ manquant
│   └── guide_installation.md                ⏳
├── data/                                    ✅
├── ingestion.py                             ✅ Douaa
├── check_db.py                              ✅ Douaa
├── transform_data/                          ✅ Hasena + Hajar
├── data_quality_check.py                    ✅ Hajar
├── orchestration/                           ✅ Zainab
├── ML/
│   ├── prepare_data.ipynb                   ✅ Yousera
│   ├── feature_engineering.ipynb            ✅ Yousera
│   ├── preprocessing.ipynb                  ✅ Yousera
│   ├── processed/                           ✅
│   ├── train.py                             ⏳ Jihad
│   ├── evaluate.py                          ⏳ Jihad
│   └── models/model.pkl                     ⏳ Jihad
├── mlflow_tracking/                         ⏳ Hafesa
├── api/                                     ⏳ Amina
└── monitoring/                              ⏳ Amina/Hafesa
```

---

## 🛠️ Stack technique

- **Ingestion** : `dlt`
- **Stockage** : DuckDB
- **Transformation** : dbt (`dbt-core`, `dbt-duckdb`)
- **Orchestration** : Dagster
- **ML** : scikit-learn (via Jupyter Notebooks pour la préparation)
- **Tracking d'expériences** : MLflow *(à venir)*
- **API** : FastAPI *(à venir)*
- **Conteneurisation** : Docker / docker-compose *(à venir)*
- **CI/CD** : GitHub Actions *(à venir)*

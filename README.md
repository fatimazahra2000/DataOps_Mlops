# 🚀 DataOps & MLOps Pipeline - Projet Recommandation

Ce projet constitue l'infrastructure MLOps complète pour notre système de recommandation. Il automatise le cycle de vie du modèle, du développement au déploiement, en garantissant la reproductibilité et la collaboration au sein de l'équipe.

## 👥 Équipe Projet
* **Ingénieur Infrastructure/MLOps :** Amina Bouazza
* **Membres de l'équipe :** Jihad El Betti, Hafsa El Hilali, Oumaima EL HABTI, AYMANE EL BADRY
* **Encadrant :** Nadia Chafik

## 🔗 Accès aux services (Cloud Infrastructure)
L'infrastructure est hébergée sur AWS et accessible via les points d'entrée suivants :

* **API de Prédiction (FastAPI) :** [http://34.198.55.82:8000/docs](http://34.198.55.82:8000/docs)
* **Serveur MLflow (Tracking) :** [http://34.198.55.82:5000](http://34.198.55.82:5000)

## 🛠️ Workflow de Développement
Pour maintenir la stabilité du déploiement, le workflow suivant est obligatoire :

1. **Gestion des branches :**
   - Ne travaillez jamais sur la branche `main`.
   - Créez une branche dédiée à votre tâche : `git checkout -b feature/nom-de-votre-tache`.
2. **CI/CD :**
   - Chaque `push` déclenche automatiquement les tests via GitHub Actions.
   - Vérifiez systématiquement le statut des tests avant de soumettre une modification.
3. **Intégration (PR) :**
   - Une fois vos tests validés, ouvrez une **Pull Request** vers la branche `main` pour fusionner votre travail.

## 💻 Configuration pour l'équipe
Pour connecter vos scripts d'entraînement locaux à l'infrastructure distante, ajoutez la configuration suivante en début de script :

```python
import mlflow
# Configuration de l'URI de tracking vers le serveur central
mlflow.set_tracking_uri("[http://34.198.55.82:5000](http://34.198.55.82:5000)")

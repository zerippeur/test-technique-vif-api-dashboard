# test-technique-vif-api-dashboard

Partie bonus d'un test technique à réaliser dans le cadre d'un processus de recrutement pour la société Vif.   
Voir le projet test-technique-vif pour les détails relatifs aux données et à l'entraînement du modèle.   

## DASHBOARD (Dossier dashboard)

Dashboard streamlit ayant accès aux données d'entraînement et permettant de choisir un numéro de cycle pour lequel prédire l'état de la valve.   
Le dashboard permet de choisir un numéro de cycle parmis les cycles des données d'entraînement et sélectionne les données relatives à ce cycle.   
Un bouton "predict" permet d'envoyer cet input à l'api de prédiction qui renvoie l'état de la valve avec l'indice de confiance.   

## API DE PRÉDICTION (Dossier api/)

API (FastAPI) de prédiction d'après le modèle entraîné dans le projet test-technique-vif.   
L'API charge le modèle à partir de la plateforme dagshub (mlflow) et renvoie au dashboard la prédiction pour l'input correspondant au numéro de cycle sélectionné dans le dashboard.   
Cette prédiction est composée de l'état de la valve "optimal" ou "non-optimal", ainsi que l'indice de confiance (0 < p < 1).   

## LANCEMENT DE L'API ET DU DASHBOARD

Projet créé avec poetry sur Windows 11.   
Installation de poetry :
https://python-poetry.org/docs/#installing-with-the-official-installer

Installation de python 3.10.8 (pour compatibilité tensorflow/tensorflow-io-gcs-filesystem) :   
https://www.python.org/downloads/release/python-3108/   

Création du venv poetry :   
Dans le dossier racine test-technique-vif-api-dashboard :   
```css
poetry env use /path/to/python3.10.8
poetry update
```
Puis lancer l'api :   
Dans le dossier test_technique_vif_api_dashboard :   
```css
uvicorn api.app:app --reload
```

Puis lancer le dashboard :    
```css
streamlit run dashboard/dashboard.py
```
## PROJETS GIT

### ENTRAINEMENT DU MODÈLE

https://github.com/zerippeur/test-technique-vif

### API ET DASHBOARD

https://github.com/zerippeur/test-technique-vif-api-dashboard
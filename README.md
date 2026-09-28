# Frenchcab

Chaque utilisateur dispose d'une branche créée sur ```origin/dev/```
* yassine
* svetlana
* malick
* thomas

## Ressources du projet :
[Trello](https://trello.com/b/6aba1ba41df9f2136e0e2c48)


## Structure du projet


/projet-taxi-prototype
├── .github/                # Configuration CI/CD
│   └── workflows/
│       └── ci.yml          # Pipeline de test et de build
├── .gitignore
├── README.md
Règles de contribution et installation
├── backend/
│   │   └── Dockerfile
│   ├── api/
│   ├── db/                 # Code pour la connexion et les requêtes SQL
                            # Code Node.js/Express pour l'API
    .env

└── frontend/
│       └── Dockerfile
│   └── web/                # Code Angular (Frontend)
    /environement

├── tests/                  # Tous les tests (Vitest/Jest)
├── sql/

## Contributing

**Pas de push** sur la branche ```dev``` : chacun travaille sur sa branche, les fusions sont faites uniquement après validation des tests, par l'intégrateur.

Les commits sont étiquetés en fonction du type de travail qui a été effectué.
Par exemple : 
<doc>Mise à jour de la doc
<fix>Corrrection de la ligne / fichier / fonction
<feat>Ajout de la fonctionnalité

[Ensemble des règles de contribution du projet](./CONTRIBUTING.md)

## Déploiement et lancement


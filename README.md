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

## Dictionnaire de données

| Nom de champ          | Description                                                                                                                                                                                                                                                   | Type                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| VendorID              | Code qui indique quel opérateur a fournit l'enregistrement de données.<br>**1 = Creative Mobile Technologies, LLC;<br>2 = VeriFone Inc.**                                                                                                                     | int                              |
| tpep_pickup_datetime  | Date et heure à la **mise en route** du compteur de course.                                                                                                                                                                                                   | timestamp                        |
| tpep_dropoff_datetime | Date et heure à **l'arrêt** du compteur de course.                                                                                                                                                                                                            | timestamp                        |
| passenger_count       | Nombre de passagers dans le véhicule<br>**Cette donnée est fournit par le chauffeur.**                                                                                                                                                                        | int                              |
| trip_distance         | Distance parcourue, en miles (~1,609m), de la course relevée par le compteur.                                                                                                                                                                                 | float                            |
| RateCodeID            | Code du taux de tarification finale, en effet à la fin de la course.<br>1=Taux standard<br>2=Taux pour l'aéroport JFK<br>3=Taux pour l'aéroport Newark<br>4=Taux pour les littoraux de Nassau ou Westchester<br>5=Tarif négocié<br>6=Tarif de groupe          |                                  |
| store_and_fwd_flag    | Cet indicateur signale si l'enregistrement de la course a été stocké dans la mémoire du véhicule avant d'être transmis, en général par manque d'une connexion au serveur.<br>Y= store and forward trip<br>N= not a store and forward trip                     | text -> à transformer en booleen |
| PULocationID          | La zone TLC Taxi dans laquelle le compteur de course a été déclenché.                                                                                                                                                                                         | int                              |
| DOLocationID          | La zone TLC Taxi dans laquelle le compteur de course a été arrêté.                                                                                                                                                                                            | int                              |
| payment_type          | Valeur entière qui correspond à un mode de paiement.<br>1= Credit card<br>2= Cash<br>3= No charge<br>4= Dispute - _une opposition est faite auprès de la banque par le client_<br>5= Unknown<br>6= Voided trip - _la course est annulée et n'est pas chargée_ | int                              |
| fare_amount           | Le tarif calculé par le compteur de courses (temps et distance)                                                                                                                                                                                               | float                            |
| extra                 | Charges et coûts supplémentaires. Actuellement, Cette colonne inclut la surcharge des heures de pointes ou des heures de nuit : 0,50$ ou 1$.                                                                                                                  | float                            |
| mta_tax               | Taxe MTA (réseau métropolitain) déclenchée automatiquement en fonction du RateCodeID utilisé                                                                                                                                                                  | float                            |
| tip_amount            | Ce champ est peuplé automatiquement pour prendre en compte les pourboires CB                                                                                                                                                                                  | float                            |
| tolls_amount          | Montant total des péages pris en charge sur le trajet.                                                                                                                                                                                                        | float                            |
| improvement_surcharge | Depuis 2015, une surcharge d'amélioration de $0,30 participe à la mise en conformité et à l'amélioration des équipements pour les personnes à mobilité réduite. Elle est appliquée aux taxi Jaunes et Verts                                                   | float                            |
| total_amount          | Montant total de la course facturé au client. N'inclut pas les pourboires en espèce.                                                                                                                                                                          | float                            |
| congestion_surcharge  | Montant total collecté lors d'un trajet depuis et vers l'état de New York en traversant Manhattan par le sud de la 96th rue.                                                                                                                                  | float                            |

**Données géographiques à croiser avec les points de départ et d'arrivée des trajets**

| Nom du champ | Description            | Type |
| ------------ | ---------------------- | ---- |
| locationID   | Identifiant de la zone | int  |
| borough      | Quartier               | str  |
| zone         | zone du quartier       | str  |
| service_zone | zone de service        | str  |

##  Dictionnaire de termes 'métier'

TPEP - Taxicab Passenger Enhancement Program
MTA tax - Metropolitan Commuter Transportation Mobility Tax
Congestion surcharge : 

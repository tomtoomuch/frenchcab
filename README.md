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
| store_and_fwd_flag    | Cet indicateur signale si l'enregistrement de la course a été stocké dans la mémoire du véhicule avant d'être transmis, en général par manque d'une connexion au serveur.<br>1= store and forward trip<br>0= not a store and forward trip                     | int |
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
Congestion surcharge : taxe de traversée d'unepartie spécifique de Manhattan

## ETL

### /backend/etl/extraction.py

```from __future__ import annotations```
Cela permet d'utiliser les types de données annotées dans ce script

```import argparse```
Cette bibliothèque permet de créer un programme commande ligne qui peut recevoir des arguments en ligne de commande

```import json```
Cette bibliothèque permet de travailler avec du JSON

```import time```
Cette bibliothèque permet de mesurer le temps d'exécution de certains blocs de code

```from collections import Counter```
Cette bibliothèque permet de compter les occurrences de chaque élément d'une liste

>python backend/etl/extraction.py --nrows 100000

#### Fonctionnement de l'extraction

Le fichier de données brutes téléchargées depuis [le portail de données ouvertes de la ville de New York](https://data.cityofnewyork.us/Transportation/2023-Yellow-Taxi-Trip-Data/4b4i-vvec/about_data)

```bash
backend/data/query.csv
```

Les données sont ensuite stockées dans un CSV 

```bash
backend/data/clean/
```

##### Étapes du traitement

1. le script lit les **19 colonnes** ; les 4 colonnes techniques du portail (id, version, created_at, updated_at) sont ignorées.

2. le script normalise :
    * les noms repassent au format du dictionnaire TLC (vendorid → VendorID, pulocationid → PULocationID…),
    * les dates deviennent des dates,
    * les codes des entiers,
    * les montants des décimaux

3. le script filtre ; les lignes aberrantes sont comptées puis retirées.

4. le script écrit ; une première écriture crée le fichier avec les ent^tes de colonnes, chaque enreggistrement s'ajoute ensuite à la fin

règles de nettoyage

date_invalide
date de départ ou d'arrivée illisible
impossible de calculer la durée
hors_annee
départ hors de 2023
l'export contient des courses du 31/12/2022
duree_negative_ou_nulle
arrivée avant ou à l'heure du départ
erreur de compteur
duree_sup_6h
course de plus de 6 h
compteur resté allumé (vu : 23 h pour 1,2 mile)
distance_nulle_ou_aberrante
distance ≤ 0 ou > 200 miles
distance non enregistrée
montant_negatif_ou_nul
tarif ou total ≤ 0
lignes d'annulation ou de remboursement
montant_aberrant
total > 1 000 $
saisie erronée
vendor_inconnu
VendorID hors 1, 2, 6, 7
code absent du dictionnaire
ratecode_invalide
RatecodeID hors 1–6 et 99
code absent du dictionnaire
payment_type_invalide
payment_type hors 0–6
code absent du dictionnaire

doublon

ligne identique à une autre du même morceau

double envoi

deux valeurs sont vidées sans supprimer la course : passenger_count = 0 et RatecodeID = 99 deviennent « inconnu » (case vide).
fichiers produits

deux fichiers arrivent dans backend/data/clean/ 

• yellow_tripdata_2023.csv   les courses propres, 23 colonnes (les 19 du dictionnaire + 4 ajoutées). il peut peser plusieurs Go ,vérifier l'espace disque
• rapport_extraction_2023.json  lignes lues, gardées, rejetées, taux de rejet et détail par motif.


Colonne ajoutée

cbd_congestion_fee
0 pour 2023 (taxe créée le 5 janvier 2025), gardée pour un schéma identique d'une année à l'autre
trip_duration_min
durée de la course en minutes

pickup_hour

heure de départ (0–23)

pickup_weekday

jour de départ (0 = lundi, 6 = dimanche)

Points d'attention
 Remboursements--- une annulation apparaît en deux lignes, une négative et une positive. La négative est retirée, la positive reste : la course compte donc une fois alors qu'elle a été remboursée

• doublons --- ils ne sont détectés qu'à l'intérieur d'un même morceau , deux lignes identiques dans deux morceaux différents
• frais d'aéroport, VendorID 1 : pour les courses à l'aéroport, extra semble déjà contenir les 1,25 $ de airport_fee. La somme des colonnes dépasse alors total_amount de 1,25 $ ; se fier à total_amount
•pourboires en espèces  ----- ils ne sont pas enregistrés ; tip_amount ne concerne que les paiements par carte
• improvement_surcharge : quelques lignes sont à 0,30 $ au lieu de 1,00 $ (ancien tarif) ; elles sont gardées
•test le script a été vérifié sur un petit extrait, pas encore sur les 6 Go complets

 lancer d'abord avec --nrows 100000 et relire le rapport    python backend/etl/extraction.py --nrows 100000

 ## Problématiques

Incohérences entre colonnes et tables sql -> ajouter les quelques colonnes manquantes dans la table "trajets" et  s'assurer de la présence du champ `uid_trajet` qui est un identifiant unique auutoincrémenté et fait office de clé primaire.


Congestion surcharge : 

##Backend Node.js

### routes
GET http://localhost:3001/api/courses = toute les courses (pagination a 100 première course sinon crash car trop de course)

résultat docker: 
conteneur-back  | App connecté sur le port 3001
conteneur-back  |  Connexion réussie à la base SQLite (frenchcab.db) !
conteneur-back  | Erreur SQL : null
conteneur-back  | Nombre de courses : 100

GET http://localhost:3001/api/courseID?id=1 = course par ID

## connexion db 

fichié connexion.js pour ce connecter à la db pas d'identifiant ou mdp pour ce connecter car c'est une db sqlite3

// Cible le dossier 'data' puis le fichier 'french.db' depuis l'emplacement de ce fichier
const dbPath = path.resolve(__dirname, 'frenchcab.db'); changer le nom selon votre bdd

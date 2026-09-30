from __future__ import annotations cela permet d'utiliser les types de données annotées dans ce script

import argparse  cette bibliothèque permet de créer un programme commande ligne qui peut recevoir des arguments en ligne de commande

import json  cette bibliothèque permet de travailler avec du JSON

import time  cette bibliothèque permet de mesurer le temps d'exécution de certains blocs de code

from collections import Counter : Cette bibliothèque permet de compter les occurrences de chaque élément d'une liste


python backend/etl/extraction.py --nrows 100000

python backend/etl/extraction.py   

backend/data/query.csv

Fichier source
backend/data/clean/


renomme et type sans supprimer de lignes
Étapes du tr



aitement

1. lire les 19 colonnes; les 4 colonnes techniques du portail (id, version, created_at, updated_at) sont ignorées
2. transformer  les noms repassent au format du dictionnaire TLC (vendorid → VendorID, pulocationid → PULocationID…), les dates deviennent des dates, les codes des entiers, les montants des décimaux
3.filtrer  les lignes aberrantes sont retirées et comptées 
4.écrire  le premier morceau crée le fichier avec l'en-tête, les suivants s'ajoutent à la fin

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
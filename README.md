# Journal de Bord - Migration MySQL vers PostgreSQL

**Groupe :** [Vos Noms]
**Projet :** td-migration-lvl1

## Description
Ce projet documente la migration d'une base de données `ReservationVoyage` depuis MySQL vers PostgreSQL.

## Architecture
- **Source** : MySQL 8.0 (Port 3306)
- **Cible** : PostgreSQL 16 (Port 5432)
- **Outils** : Docker, Python (Faker), Flyway

## Étapes Réalisées

### 1. Initialisation de l'environnement
- Création du `docker-compose.yml` pour orchestrer les conteneurs SGBD.
- Lancement des conteneurs validé.

### 2. Peuplement de la Source (MySQL)
- Création d'un script Python `populate_mysql.py` utilisant Faker.
- Génération de :
    - 500 Utilisateurs
    - 1000 Réservations

### 3. Migration (Flyway)
- Extraction des données MySQL vers des scripts compatibles PostgreSQL.
- Création des scripts de versioning Flyway (`V1`, `V2`, etc.).
- Exécution de la migration via Docker.

### 4. Tests
- Scripts de vérification d'intégrité et de complétude exécutés sur PostgreSQL.

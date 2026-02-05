# 🚀 TD Migration de Base de Données - MySQL vers PostgreSQL

**Groupe :** Wassim, Mohamed, Johan, Feras, Karim, Matheo
**Module :** Infrastructure & DevOps  
**Date :** Février 2026

---

## 📋 Description du Projet

Ce projet documente la **migration complète** d'une base de données de réservation de voyages depuis **MySQL 8.0** vers **PostgreSQL 16**, en utilisant une approche DevOps moderne avec **Docker** et **Flyway**.

### Objectifs atteints :
- ✅ **Niveau 1** : Installation des outils et peuplement de la base MySQL
- ✅ **Niveau 2** : Migration automatisée avec Docker et Flyway
- ✅ **Niveau 3** : Tests d'intégrité et de complétude

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │
│   MySQL 8.0     │ ──────► │  PostgreSQL 16  │
│   (Source)      │  Flyway │   (Cible)       │
│   Port: 3306    │         │   Port: 5432    │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
        ▲                           │
        │                           │
    Faker                      Vérification
   (500 users)                 (Tests SQL)
  (1000 résa)
```

---

## 📁 Structure du Projet

```
td-migration-bdd/
│
├── 📄 docker-compose.yml       # Orchestration des conteneurs MySQL & PostgreSQL
├── 📄 Dockerfile.scripts       # Image Docker pour exécuter les scripts Python
├── 📄 requirements.txt         # Dépendances Python (pymysql, Faker, psycopg2)
├── 📄 README.md                # Ce fichier (Journal de bord)
├── 📄 .gitignore
│
├── 📂 scripts/
│   ├── populate_mysql.py       # Génère 500 users + 1000 réservations dans MySQL
│   └── extract_to_flyway.py    # Extrait les données MySQL vers un script SQL
│
└── 📂 flyway_migration/
    ├── 📂 conf/
    │   └── flyway.conf         # Configuration Flyway (connexion PostgreSQL)
    │
    └── 📂 sql/
        ├── V1__Create_tables.sql      # Création du schéma PostgreSQL
        ├── V2__Insert_data.sql        # Données migrées (généré automatiquement)
        ├── V3__Test_integrite.sql     # Tests d'intégrité (NULLs, FK)
        └── V4__Test_completude.sql    # Tests de volumétrie (counts)
```

---

## 🔧 Prérequis

- **Docker Desktop** (Windows/Mac) ou Docker Engine (Linux)
- **Python 3.9+** (optionnel, les scripts tournent dans Docker)
- **Git**

---

## 🚀 Guide d'Installation et d'Exécution

### Étape 1 : Cloner le dépôt

```bash
git clone https://github.com/0xBlxck/td-migration-lvl1-Wassim-Mohamed-Johan-Feras-Karim-Matheo.git
cd td-migration-lvl1-Wassim-Mohamed-Johan-Feras-Karim-Matheo
```

### Étape 2 : Lancer les bases de données

```bash
docker compose up -d
```

Vérifier que les conteneurs tournent :
```bash
docker ps
```

Résultat attendu :
```
NAMES             STATUS                  PORTS
mysql-source      Up X minutes (healthy)  0.0.0.0:3306->3306/tcp
postgres-target   Up X minutes (healthy)  0.0.0.0:5432->5432/tcp
```

### Étape 3 : Peupler MySQL avec des données de test

```bash
# Construire l'image des scripts
docker build -f Dockerfile.scripts -t migration-scripts .

# Exécuter le script de peuplement
docker run --rm --network td-migration-bdd_default migration-scripts
```

Résultat attendu :
```
En attente de MySQL...
MySQL est prêt !
Création de la base ReservationVoyage...
Création de la table Utilisateurs...
Création de la table Reservations...
Génération de 500 utilisateurs...
✓ 500 utilisateurs insérés.
Génération de 1000 réservations...
✓ 1000 réservations insérées.
🎉 Base MySQL peuplée avec succès !
```

### Étape 4 : Extraire les données pour la migration

```bash
docker run --rm --network td-migration-bdd_default \
  -v "${PWD}/flyway_migration:/app/flyway_migration" \
  migration-scripts python scripts/extract_to_flyway.py
```

Résultat attendu :
```
Connexion à MySQL...
Extraction Utilisateurs...
✓ 500 utilisateurs extraits.
Extraction Reservations...
✓ 1000 réservations extraites.
🎉 Extraction terminée dans flyway_migration/sql/V2__Insert_data.sql !
```

### Étape 5 : Exécuter la migration Flyway

```bash
docker run --rm --network td-migration-bdd_default \
  -v "${PWD}/flyway_migration/sql:/flyway/sql" \
  -v "${PWD}/flyway_migration/conf:/flyway/conf" \
  flyway/flyway -configFiles="/flyway/conf/flyway.conf" migrate
```

### Étape 6 : Vérifier la migration

```bash
docker exec postgres-target psql -U postgres -d reservation_voyage \
  -c "SELECT COUNT(*) as utilisateurs FROM utilisateurs; SELECT COUNT(*) as reservations FROM reservations;"
```

Résultat attendu :
```
 utilisateurs 
--------------
          500

 reservations
--------------
         1000
```

---

## 🧪 Tests d'Intégrité (Niveau 3)

### Test 1 : Absence de valeurs NULL critiques

```sql
SELECT count(*) as erreurs_email_null FROM utilisateurs WHERE email IS NULL;
-- Résultat attendu: 0
```

### Test 2 : Intégrité des clés étrangères

```sql
SELECT count(*) as resa_orphelines 
FROM reservations r 
LEFT JOIN utilisateurs u ON r.utilisateur_id = u.id 
WHERE u.id IS NULL;
-- Résultat attendu: 0
```

### Test 3 : Volumétrie

```sql
SELECT count(*) as total_utilisateurs FROM utilisateurs;
-- Résultat attendu: 500

SELECT count(*) as total_reservations FROM reservations;
-- Résultat attendu: 1000
```

**✅ Tous les tests passent avec succès !**

---

## 📊 Schéma de la Base de Données

### MySQL (Source)

```sql
CREATE TABLE Utilisateurs (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Prenom VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    MotDePasse VARCHAR(255) NOT NULL
);

CREATE TABLE Reservations (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UtilisateurId INT NOT NULL,
    Destination VARCHAR(100) NOT NULL,
    DateReservation DATE NOT NULL,
    Prix DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (UtilisateurId) REFERENCES Utilisateurs(Id)
);
```

### PostgreSQL (Cible)

```sql
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    date_creation TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    destination VARCHAR(100) NOT NULL,
    date_reservation TIMESTAMP NOT NULL,
    prix DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
);
```

---

## 🔄 Différences de Syntaxe MySQL vs PostgreSQL

| Élément       | MySQL               | PostgreSQL          |
|--------------|---------------------|---------------------|
| Auto-increment | `AUTO_INCREMENT`   | `SERIAL`            |
| Booléen       | `TINYINT(1)`       | `BOOLEAN`           |
| Date/Heure    | `DATETIME`         | `TIMESTAMP`         |
| Guillemets    | \`backticks\`      | "double quotes"     |
| LIMIT         | `LIMIT 10, 5`      | `LIMIT 5 OFFSET 10` |

---

## 📅 Journal de Bord

| Date       | Étape                                      | Statut |
|------------|-------------------------------------------|--------|
| 02/02/2026 | Création du docker-compose.yml            | ✅     |
| 02/02/2026 | Script populate_mysql.py avec Faker       | ✅     |
| 02/02/2026 | Génération de 500 users + 1000 résa       | ✅     |
| 02/02/2026 | Configuration Flyway                      | ✅     |
| 02/02/2026 | Script extract_to_flyway.py               | ✅     |
| 02/02/2026 | Migration Flyway V1 → V4                  | ✅     |
| 02/02/2026 | Tests d'intégrité passés                  | ✅     |
| 02/02/2026 | Commit Git initial                        | ✅     |

---

## 👥 Équipe

- **Wassim**
- **Mohamed**
- **Johan**
- **Feras**
- **Karim**
- **Matheo**

---

## 📚 Références

1. [Bytebase - How to Migrate from MySQL to PostgreSQL](https://www.bytebase.com/reference/migration/how-to-migrate-database-from-mysql-to-postgres/)
2. [Flyway Documentation](https://flywaydb.org/documentation/)
3. [Docker Compose Documentation](https://docs.docker.com/compose/)
4. [Python Faker Library](https://faker.readthedocs.io/)

---

## 📜 Licence

Ce projet est réalisé dans le cadre d'un TD académique à l'EPSI.

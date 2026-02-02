import pymysql
from faker import Faker
import random
import time

# Configuration
DB_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'root',
    'port': 3306
}
DB_NAME = 'ReservationVoyage'

def wait_for_db():
    """Attendre que la BDD soit prête"""
    print("En attente de MySQL...")
    for i in range(30):
        try:
            conn = pymysql.connect(**DB_CONFIG)
            conn.close()
            print("\nMySQL est prêt !")
            return True
        except pymysql.Error as e:
            print(".", end="", flush=True)
            time.sleep(1)
    print("\nTimeout: MySQL n'est pas accessible")
    return False

def init_db():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Création BDD
        print(f"Création de la base {DB_NAME}...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {DB_NAME}")
        
        # Table Utilisateurs
        print("Création de la table Utilisateurs...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Utilisateurs (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            Nom VARCHAR(100) NOT NULL,
            Prenom VARCHAR(100) NOT NULL,
            Email VARCHAR(255) NOT NULL UNIQUE,
            MotDePasse VARCHAR(255) NOT NULL
        )
        """)
        
        # Table Reservations
        print("Création de la table Reservations...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reservations (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            UtilisateurId INT NOT NULL,
            Destination VARCHAR(100) NOT NULL,
            DateReservation DATE NOT NULL,
            Prix DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (UtilisateurId) REFERENCES Utilisateurs(Id)
        )
        """)
        
        conn.commit()
        return conn
    except pymysql.Error as err:
        print(f"Erreur : {err}")
        return None

def populate_data(conn):
    fake = Faker('fr_FR')
    cursor = conn.cursor()
    
    # Vérifier si des données existent déjà
    cursor.execute("SELECT COUNT(*) FROM Utilisateurs")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"La base contient déjà {count} utilisateurs. Abandon.")
        return
    
    # Génération Utilisateurs
    print("Génération de 500 utilisateurs...")
    users = []
    emails = set()
    
    while len(users) < 500:
        prenom = fake.first_name()
        nom = fake.last_name()
        email = f"{prenom.lower()}.{nom.lower()}{random.randint(1,999)}@{fake.free_email_domain()}"
        
        if email not in emails:
            emails.add(email)
            users.append((nom, prenom, email, fake.password()))
            
    cursor.executemany(
        "INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse) VALUES (%s, %s, %s, %s)",
        users
    )
    conn.commit()
    print("✓ 500 utilisateurs insérés.")
    
    # Récupérer les IDs des utilisateurs créés
    cursor.execute("SELECT Id FROM Utilisateurs")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    # Génération Réservations
    print("Génération de 1000 réservations...")
    reservations = []
    for _ in range(1000):
        reservations.append((
            random.choice(user_ids),
            fake.city(),
            fake.date_this_year(),
            round(random.uniform(50.0, 2000.0), 2)
        ))
        
    cursor.executemany(
        "INSERT INTO Reservations (UtilisateurId, Destination, DateReservation, Prix) VALUES (%s, %s, %s, %s)",
        reservations
    )
    conn.commit()
    print("✓ 1000 réservations insérées.")

if __name__ == "__main__":
    if wait_for_db():
        conn = init_db()
        if conn:
            populate_data(conn)
            conn.close()
            print("\n🎉 Base MySQL peuplée avec succès !")

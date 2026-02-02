import pymysql

# Config - Utilise le nom du service Docker
MYSQL_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'root',
    'database': 'ReservationVoyage',
    'port': 3306
}
OUTPUT_FILE = 'flyway_migration/sql/V2__Insert_data.sql'

def extract():
    try:
        print("Connexion à MySQL...")
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("-- V2__Insert_data.sql\n")
            f.write("-- Données extraites depuis MySQL\n\n")
            
            # 1. Utilisateurs
            print("Extraction Utilisateurs...")
            cursor.execute("SELECT Id, Nom, Prenom, Email, MotDePasse FROM Utilisateurs")
            users = cursor.fetchall()
            
            if users:
                f.write("INSERT INTO utilisateurs (id, nom, prenom, email, mot_de_passe) VALUES\n")
                values = []
                for u in users:
                    # Echapper les single quotes dans les chaines
                    nom = u[1].replace("'", "''")
                    prenom = u[2].replace("'", "''")
                    email = u[3].replace("'", "''")
                    mdp = u[4].replace("'", "''")
                    values.append(f"({u[0]}, '{nom}', '{prenom}', '{email}', '{mdp}')")
                f.write(",\n".join(values) + ";\n\n")
                print(f"✓ {len(users)} utilisateurs extraits.")

            # 2. Reservations
            print("Extraction Reservations...")
            cursor.execute("SELECT Id, UtilisateurId, Destination, DateReservation, Prix FROM Reservations")
            resas = cursor.fetchall()
            
            if resas:
                f.write("INSERT INTO reservations (id, utilisateur_id, destination, date_reservation, prix) VALUES\n")
                values = []
                for r in resas:
                    dest = r[2].replace("'", "''")
                    date = r[3].strftime('%Y-%m-%d %H:%M:%S')
                    prix = r[4]
                    values.append(f"({r[0]}, {r[1]}, '{dest}', '{date}', {prix})")
                f.write(",\n".join(values) + ";\n")
                print(f"✓ {len(resas)} réservations extraites.")
                
            # Reset des séquences (Important pour PostgreSQL après insertion manuelle d'IDs)
            f.write("\n-- Mise à jour des séquences\n")
            f.write("SELECT setval('utilisateurs_id_seq', (SELECT MAX(id) FROM utilisateurs));\n")
            f.write("SELECT setval('reservations_id_seq', (SELECT MAX(id) FROM reservations));\n")

        print(f"\n🎉 Extraction terminée dans {OUTPUT_FILE} !")
        
    except Exception as e:
        print(f"Erreur : {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

if __name__ == "__main__":
    extract()

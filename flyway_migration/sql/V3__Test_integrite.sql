-- V3__Test_integrite.sql
-- Vérifications post-migration

-- 1. Vérifier qu'il n'y a pas d'utilisateurs sans email (Règle métier)
SELECT count(*) as erreurs_email_null FROM utilisateurs WHERE email IS NULL;

-- 2. Vérifier l'intégrité des clés étrangères (Orphelins ?)
-- Si count > 0, c'est qu'on a des réservations sans utilisateur
SELECT count(*) as resa_orphelines 
FROM reservations r 
LEFT JOIN utilisateurs u ON r.utilisateur_id = u.id 
WHERE u.id IS NULL;

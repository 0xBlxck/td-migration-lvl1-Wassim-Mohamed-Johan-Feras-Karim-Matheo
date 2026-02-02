-- V4__Test_completude.sql
-- Vérifications de volumétrie

-- Doit retourner 500
SELECT count(*) as total_utilisateurs FROM utilisateurs;

-- Doit retourner 1000
SELECT count(*) as total_reservations FROM reservations;

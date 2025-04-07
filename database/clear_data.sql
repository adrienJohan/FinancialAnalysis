-- Sélectionner la base de données
USE FinancialAnalysis;

-- Désactiver les contraintes de clés étrangères
SET FOREIGN_KEY_CHECKS = 0;

-- Vider toutes les tables
TRUNCATE TABLE PriceNews;
TRUNCATE TABLE News;
TRUNCATE TABLE Prices;
TRUNCATE TABLE ForexData;
TRUNCATE TABLE EconomicData;

-- Réactiver les contraintes de clés étrangères
SET FOREIGN_KEY_CHECKS = 1;

-- Confirmation
SELECT 'Tables vidées avec succès' AS Message;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: centre_formation
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appels`
--

DROP TABLE IF EXISTS `appels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lead_id` int(11) NOT NULL,
  `date_appel` datetime DEFAULT NULL,
  `canal` enum('tel','whatsapp') DEFAULT NULL,
  `resultat` enum('joignable','non_joignable','rappeler','RDV') DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `prochain_rappel_at` datetime DEFAULT NULL,
  `dernier_rappel_at` datetime DEFAULT NULL,
  `nb_rappels_programmes` int(11) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `lead_id` (`lead_id`),
  CONSTRAINT `appels_ibfk_1` FOREIGN KEY (`lead_id`) REFERENCES `leads` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `echeances`
--

DROP TABLE IF EXISTS `echeances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `echeances` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `facture_id` int(11) NOT NULL,
  `libelle` varchar(255) DEFAULT NULL,
  `montant_du` decimal(10,2) DEFAULT NULL,
  `date_echeance` date DEFAULT NULL,
  `date_tolerance` date DEFAULT NULL,
  `statut` enum('du','partiellement_regle','regle','en_retard') DEFAULT 'du',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `facture_id` (`facture_id`),
  CONSTRAINT `echeances_ibfk_1` FOREIGN KEY (`facture_id`) REFERENCES `factures` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `enfants`
--

DROP TABLE IF EXISTS `enfants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enfants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `num_tel_papa` varchar(20) DEFAULT NULL,
  `num_tel_maman` varchar(20) DEFAULT NULL,
  `num_tel_enfant` varchar(20) DEFAULT NULL,
  `sexe` enum('M','F') DEFAULT NULL,
  `niveau_scolaire` varchar(100) DEFAULT NULL,
  `niveau_avant_centre` tinyint(1) DEFAULT 0,
  `remarques` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `enfants_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `leads` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `factures`
--

DROP TABLE IF EXISTS `factures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inscription_id` int(11) NOT NULL,
  `numero` varchar(50) DEFAULT NULL,
  `date_emission` date DEFAULT NULL,
  `total_ht` decimal(10,2) DEFAULT NULL,
  `total_taxes` decimal(10,2) DEFAULT NULL,
  `total_ttc` decimal(10,2) DEFAULT NULL,
  `statut` enum('brouillon','emis','partiellement_regle','regle','annulee') DEFAULT 'brouillon',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero` (`numero`),
  KEY `inscription_id` (`inscription_id`),
  CONSTRAINT `factures_ibfk_1` FOREIGN KEY (`inscription_id`) REFERENCES `inscriptions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `formateur_pointage`
--

DROP TABLE IF EXISTS `formateur_pointage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `formateur_pointage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formateur_id` int(11) NOT NULL,
  `seance_id` int(11) NOT NULL,
  `heure_debut` datetime DEFAULT NULL,
  `heure_fin` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `formateur_id` (`formateur_id`),
  KEY `seance_id` (`seance_id`),
  CONSTRAINT `formateur_pointage_ibfk_1` FOREIGN KEY (`formateur_id`) REFERENCES `formateurs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `formateur_pointage_ibfk_2` FOREIGN KEY (`seance_id`) REFERENCES `seances` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `formateur_sessions`
--

DROP TABLE IF EXISTS `formateur_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `formateur_sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formateur_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `role` enum('principal','assistant') DEFAULT 'principal',
  `date_affectation` date DEFAULT NULL,
  `statut` enum('actif','clos') DEFAULT 'actif',
  PRIMARY KEY (`id`),
  KEY `formateur_id` (`formateur_id`),
  KEY `session_id` (`session_id`),
  CONSTRAINT `formateur_sessions_ibfk_1` FOREIGN KEY (`formateur_id`) REFERENCES `formateurs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `formateur_sessions_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `formateurs`
--

DROP TABLE IF EXISTS `formateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `formateurs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `date_arrivee` date DEFAULT NULL,
  `date_depart` date DEFAULT NULL,
  `disponibilites` text DEFAULT NULL,
  `statut` enum('actif','inactif') DEFAULT 'actif',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `formations`
--

DROP TABLE IF EXISTS `formations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `formations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `actif` tinyint(1) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inscriptions`
--

DROP TABLE IF EXISTS `inscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inscriptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lead_id` int(11) NOT NULL,
  `enfant_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `statut` enum('preinscrit','inscrit','abandon','termine') DEFAULT 'preinscrit',
  `date_inscription` date DEFAULT NULL,
  `prix_negocie` decimal(10,2) DEFAULT NULL,
  `remise_total` decimal(10,2) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `lead_id` (`lead_id`),
  KEY `enfant_id` (`enfant_id`),
  KEY `session_id` (`session_id`),
  CONSTRAINT `inscriptions_ibfk_1` FOREIGN KEY (`lead_id`) REFERENCES `leads` (`id`),
  CONSTRAINT `inscriptions_ibfk_2` FOREIGN KEY (`enfant_id`) REFERENCES `enfants` (`id`),
  CONSTRAINT `inscriptions_ibfk_3` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `leads`
--

DROP TABLE IF EXISTS `leads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `whatsapp_url` varchar(255) DEFAULT NULL,
  `disponibilites` text DEFAULT NULL,
  `statut_pipeline` enum('nouveau','contact','RDV','converti','perdu') DEFAULT 'nouveau',
  `source` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paiements`
--

DROP TABLE IF EXISTS `paiements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paiements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inscription_id` int(11) DEFAULT NULL,
  `facture_id` int(11) DEFAULT NULL,
  `echeance_id` int(11) DEFAULT NULL,
  `date_paiement` datetime DEFAULT NULL,
  `montant` decimal(10,2) DEFAULT NULL,
  `moyen` enum('espèces','virement','carte','chèque','autre') DEFAULT NULL,
  `statut` enum('recu','en_attente','refuse','rembourse_partiel','rembourse_total') DEFAULT 'recu',
  `encaisse_par` int(11) DEFAULT NULL,
  `justificatif_url` varchar(255) DEFAULT NULL,
  `commentaire` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `inscription_id` (`inscription_id`),
  KEY `facture_id` (`facture_id`),
  KEY `echeance_id` (`echeance_id`),
  CONSTRAINT `paiements_ibfk_1` FOREIGN KEY (`inscription_id`) REFERENCES `inscriptions` (`id`),
  CONSTRAINT `paiements_ibfk_2` FOREIGN KEY (`facture_id`) REFERENCES `factures` (`id`),
  CONSTRAINT `paiements_ibfk_3` FOREIGN KEY (`echeance_id`) REFERENCES `echeances` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paies_formateur`
--

DROP TABLE IF EXISTS `paies_formateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paies_formateur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formateur_id` int(11) NOT NULL,
  `periode_debut` date DEFAULT NULL,
  `periode_fin` date DEFAULT NULL,
  `montant_du` decimal(10,2) DEFAULT NULL,
  `montant_paye` decimal(10,2) DEFAULT NULL,
  `date_paiement` date DEFAULT NULL,
  `statut` enum('du','partiel','regle') DEFAULT 'du',
  `reference_externe` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `formateur_id` (`formateur_id`),
  CONSTRAINT `paies_formateur_ibfk_1` FOREIGN KEY (`formateur_id`) REFERENCES `formateurs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paies_formateur_lignes`
--

DROP TABLE IF EXISTS `paies_formateur_lignes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paies_formateur_lignes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paie_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `seance_id` int(11) NOT NULL,
  `enfant_id` int(11) NOT NULL,
  `coef_applique` decimal(10,2) DEFAULT NULL,
  `montant_ligne` decimal(10,2) DEFAULT NULL,
  `commentaire` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `paie_id` (`paie_id`),
  KEY `session_id` (`session_id`),
  KEY `seance_id` (`seance_id`),
  KEY `enfant_id` (`enfant_id`),
  CONSTRAINT `paies_formateur_lignes_ibfk_1` FOREIGN KEY (`paie_id`) REFERENCES `paies_formateur` (`id`) ON DELETE CASCADE,
  CONSTRAINT `paies_formateur_lignes_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`) ON DELETE CASCADE,
  CONSTRAINT `paies_formateur_lignes_ibfk_3` FOREIGN KEY (`seance_id`) REFERENCES `seances` (`id`) ON DELETE CASCADE,
  CONSTRAINT `paies_formateur_lignes_ibfk_4` FOREIGN KEY (`enfant_id`) REFERENCES `enfants` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `presences_enfant`
--

DROP TABLE IF EXISTS `presences_enfant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presences_enfant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `enfant_id` int(11) NOT NULL,
  `seance_id` int(11) NOT NULL,
  `present` tinyint(1) DEFAULT 1,
  `remarque` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `enfant_id` (`enfant_id`),
  KEY `seance_id` (`seance_id`),
  CONSTRAINT `presences_enfant_ibfk_1` FOREIGN KEY (`enfant_id`) REFERENCES `enfants` (`id`) ON DELETE CASCADE,
  CONSTRAINT `presences_enfant_ibfk_2` FOREIGN KEY (`seance_id`) REFERENCES `seances` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seances`
--

DROP TABLE IF EXISTS `seances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seances` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_id` int(11) NOT NULL,
  `date_debut` datetime DEFAULT NULL,
  `date_fin` datetime DEFAULT NULL,
  `type` enum('cours','rattrapage','essai','autre') DEFAULT 'cours',
  `statut` enum('prévue','réalisée','annulée') DEFAULT 'prévue',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `session_id` (`session_id`),
  CONSTRAINT `seances_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formation_id` int(11) NOT NULL,
  `nom_session` varchar(255) NOT NULL,
  `prix_base` decimal(10,2) DEFAULT NULL,
  `date_debut` date DEFAULT NULL,
  `date_fin` date DEFAULT NULL,
  `statut` enum('planifiée','en_cours','terminée','annulée') DEFAULT 'planifiée',
  `paiement_coef` decimal(10,2) DEFAULT 37.50,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `formation_id` (`formation_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`formation_id`) REFERENCES `formations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-14 22:04:07

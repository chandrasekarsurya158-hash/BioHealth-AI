-- ====================================================================
-- Database Schema: Multi-Domain AI Disease Detection & Health Assistant
-- Target Database: MySQL (XAMPP / phpMyAdmin)
-- Normalized 3NF Architecture with Foreign Keys and Indexes
-- ====================================================================

CREATE DATABASE IF NOT EXISTS `multi_disease_db`
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `multi_disease_db`;

-- --------------------------------------------------------------------
-- 1. Users Table (Core account management)
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `fullname` VARCHAR(120) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `role` VARCHAR(20) NOT NULL DEFAULT 'user',
    `password_hash` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_user_email` (`email`),
    INDEX `idx_user_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 2. Admins Table (Administrative and research privileges)
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `admins` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(80) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `fullname` VARCHAR(120) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_admin_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 3. Module 1: Plant Disease Detection Results
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `plant_detection_results` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `image_path` VARCHAR(255) NOT NULL,
    `predicted_class` VARCHAR(120) NOT NULL,
    `confidence` DECIMAL(5, 2) NOT NULL,
    `disease_info` TEXT,
    `prevention_methods` TEXT,
    `is_healthy` BOOLEAN DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
    INDEX `idx_plant_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 4. Module 2: Crop Disease Detection Results (Rice, Wheat, Maize)
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `crop_detection_results` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `crop_type` ENUM('rice', 'wheat', 'maize') NOT NULL,
    `image_path` VARCHAR(255) NOT NULL,
    `predicted_class` VARCHAR(120) NOT NULL,
    `confidence` DECIMAL(5, 2) NOT NULL,
    `symptoms` TEXT,
    `prevention_info` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
    INDEX `idx_crop_user` (`user_id`),
    INDEX `idx_crop_type` (`crop_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 5. Module 3: Skin Disease Screening Results
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `skin_screening_results` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `image_path` VARCHAR(255) NOT NULL,
    `predicted_category` VARCHAR(120) NOT NULL,
    `confidence` DECIMAL(5, 2) NOT NULL,
    `risk_notes` TEXT,
    `disclaimer_agreed` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
    INDEX `idx_skin_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 6. Module 4A: Symptoms-Based Health Assessments
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `symptom_assessments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `symptoms_json` JSON NOT NULL,
    `duration` VARCHAR(60) NOT NULL,
    `severity` ENUM('mild', 'moderate', 'severe') NOT NULL,
    `additional_notes` TEXT,
    `possible_explanations` TEXT,
    `urgency_level` ENUM('low', 'moderate', 'high', 'emergency') NOT NULL,
    `warning_flags` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
    INDEX `idx_symptoms_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 7. Module 4B: Blood Reports (Documents & Summaries)
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `blood_reports` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `file_path` VARCHAR(255) NOT NULL,
    `file_type` VARCHAR(20) NOT NULL,
    `extracted_text` MEDIUMTEXT,
    `overall_summary` TEXT,
    `disclaimer` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
    INDEX `idx_blood_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 8. Module 4B: Individual Blood Test Biomarkers (Normalized 1:N)
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `blood_test_values` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `report_id` INT NOT NULL,
    `test_name` VARCHAR(100) NOT NULL,
    `measured_value` VARCHAR(50) NOT NULL,
    `unit` VARCHAR(30),
    `reference_range` VARCHAR(60),
    `flag` ENUM('NORMAL', 'HIGH', 'LOW', 'INDETERMINATE') DEFAULT 'NORMAL',
    `clinical_meaning` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`report_id`) REFERENCES `blood_reports`(`id`) ON DELETE CASCADE,
    INDEX `idx_report_id` (`report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 9. Module 4C: Chest X-Ray Research Results
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `xray_results` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `image_path` VARCHAR(255) NOT NULL,
    `predicted_category` VARCHAR(120) NOT NULL,
    `confidence` DECIMAL(5, 2) NOT NULL,
    `radiologist_disclaimer` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
    INDEX `idx_xray_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 10. Module 4E: Verified Medicines Knowledge Base
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `medicines` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(120) NOT NULL,
    `generic_name` VARCHAR(150),
    `category` VARCHAR(80),
    `uses` TEXT NOT NULL,
    `side_effects` TEXT NOT NULL,
    `precautions` TEXT NOT NULL,
    `warnings` TEXT NOT NULL,
    `last_reviewed_date` DATE NOT NULL,
    INDEX `idx_medicine_name` (`name`),
    INDEX `idx_generic_name` (`generic_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 11. Module 4E: Medicine References & Sources (Normalized 1:N)
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `medicine_references` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `medicine_id` INT NOT NULL,
    `source_name` VARCHAR(150) NOT NULL,
    `reference_url` VARCHAR(255),
    `publisher` VARCHAR(150),
    `edition_year` INT,
    FOREIGN KEY (`medicine_id`) REFERENCES `medicines`(`id`) ON DELETE CASCADE,
    INDEX `idx_medicine_id` (`medicine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 12. Cross-Module Unified Analysis History
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `analysis_history` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `module_type` ENUM('plant', 'crop', 'skin', 'symptoms', 'blood_report', 'xray') NOT NULL,
    `record_id` INT NOT NULL,
    `summary_label` VARCHAR(150) NOT NULL,
    `confidence_or_status` VARCHAR(50),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    INDEX `idx_history_user` (`user_id`),
    INDEX `idx_history_module` (`module_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------------------
-- 13. System Administration & Role-Based Activity Logs
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `admin_activity_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `admin_id` INT NULL,
    `admin_name` VARCHAR(100) NOT NULL,
    `action` VARCHAR(100) NOT NULL,
    `target_module` VARCHAR(100) NOT NULL,
    `details` TEXT,
    `ip_address` VARCHAR(45),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_admin_log` (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


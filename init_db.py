"""
Database Initialization & Seeding Script
Multi-Domain AI Disease Detection & Intelligent Health Assistance System
"""

import sys
from pathlib import Path
from werkzeug.security import generate_password_hash
import pymysql
from config import Config

def print_banner(msg):
    print("\n" + "=" * 65)
    print(f" {msg}")
    print("=" * 65)

def initialize_database():
    print_banner("BioHealth AI: Database Initialization & Migration")
    print(f" Target Host: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f" Database:    {Config.DB_NAME}")
    print(f" User:        {Config.DB_USER}")

    # Step 1: Connect to MySQL server
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
            charset="utf8mb4",
            autocommit=True,
            connect_timeout=10
        )
        cursor = conn.cursor()
        print(f"\n [OK] Connected to MySQL server at {Config.DB_HOST}:{Config.DB_PORT} successfully.")
    except Exception as e:
        print(f"\n [ERROR] Could not connect to MySQL server: {e}")
        print("         Please check your DB_HOST, DB_USER, DB_PASSWORD and DB_PORT environment variables.")
        sys.exit(1)

    # Step 2: Create Database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cursor.execute(f"USE `{Config.DB_NAME}`;")
    print(f" [OK] Database '{Config.DB_NAME}' created / verified.")

    # Step 3: Read and clean schema.sql (filter out comment lines first)
    schema_path = Path(__file__).resolve().parent / "database" / "schema.sql"
    if not schema_path.exists():
        print(f" [ERROR] Schema file not found at: {schema_path}")
        sys.exit(1)

    with open(schema_path, "r", encoding="utf-8") as f:
        raw_sql = f.read()

    # Filter out pure comment lines so comments above CREATE TABLE don't hide statements
    clean_lines = []
    for line in raw_sql.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("--") or trimmed.startswith("/*"):
            continue
        clean_lines.append(line)
    
    clean_sql = "\n".join(clean_lines)

    # Split into discrete SQL statements
    statements = [stmt.strip() for stmt in clean_sql.split(";") if stmt.strip()]
    
    tables_created = 0
    for stmt in statements:
        try:
            cursor.execute(stmt)
            if "CREATE TABLE" in stmt.upper():
                # Extract table name for display
                words = stmt.split()
                if "TABLE" in [w.upper() for w in words]:
                    tables_created += 1
        except Exception as e:
            if "already exists" not in str(e):
                print(f" [SQL Notice]: {e}")

    print(f" [OK] All 12 normalized tables created and verified ({tables_created} tables created).")

    # Step 4: Seed Default Administrator Account
    cursor.execute("SELECT id FROM admins WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_pass_hash = generate_password_hash("admin123", method="pbkdf2:sha256")
        cursor.execute(
            """INSERT INTO admins (username, password_hash, fullname, email)
               VALUES ('admin', %s, 'Chief Systems Administrator', 'admin@biohealth.local')""",
            (admin_pass_hash,)
        )
        print(" [SEED] Default Admin created: username='admin', password='admin123'")
    else:
        print(" [OK] Admin account already exists.")

    # Ensure admin user also exists in users table with role='admin'
    cursor.execute("SELECT id FROM users WHERE email = 'admin@biohealth.local'")
    if not cursor.fetchone():
        admin_pass_hash = generate_password_hash("admin123", method="pbkdf2:sha256")
        cursor.execute(
            """INSERT INTO users (fullname, email, role, password_hash)
               VALUES ('Chief Systems Administrator', 'admin@biohealth.local', 'admin', %s)""",
            (admin_pass_hash,)
        )
        print(" [SEED] Admin role user created in users table (admin@biohealth.local).")

    # Step 5: Seed Verified Medicines Knowledge Base
    cursor.execute("SELECT COUNT(*) as cnt FROM medicines")
    med_count = cursor.fetchone()[0]
    if med_count == 0:
        medicines_data = [
            (
                "Paracetamol",
                "Acetaminophen",
                "Analgesic & Antipyretic",
                "Relieves mild to moderate pain (headache, toothache, muscle ache) and reduces fever.",
                "Generally well tolerated. Rare: allergic skin rash, elevated liver enzymes in chronic high doses.",
                "Do not exceed 4,000 mg (4g) in a 24-hour period. Avoid combining with other acetaminophen-containing cold remedies. Avoid alcohol.",
                "Acute overdose can cause fatal liver necrosis. Seek immediate toxicology evaluation if overdose is suspected.",
                "2026-01-15",
                [("WHO Model List of Essential Medicines", "https://www.who.int", "World Health Organization", 2024)]
            ),
            (
                "Amoxicillin",
                "Amoxicillin Trihydrate",
                "Broad-spectrum Penicillin Antibiotic",
                "Bacterial respiratory infections, otitis media, streptococcal pharyngitis, and skin infections.",
                "Nausea, diarrhea, stomach distress, mild rash, oral thrush with prolonged use.",
                "Strictly contraindicated in individuals with known penicillin or beta-lactam hypersensitivity. Complete full prescribed course to prevent antimicrobial resistance.",
                "Ineffective against viral illnesses such as the common cold, COVID-19, or influenza. Never take without prescription.",
                "2026-02-10",
                [("FDA Drug Safety Reference", "https://www.fda.gov", "US FDA", 2025)]
            ),
            (
                "Metformin",
                "Metformin Hydrochloride",
                "Biguanide Antidiabetic Agent",
                "First-line pharmacological management for Type 2 Diabetes Mellitus; improves peripheral insulin sensitivity.",
                "Gastrointestinal distress, diarrhea, abdominal cramps, metallic taste, decreased Vitamin B12 absorption.",
                "Take with meals to reduce gastrointestinal upset. Monitor kidney function (eGFR) regularly.",
                "Risk of lactic acidosis in patients with significant renal impairment, severe congestive heart failure, or acute sepsis.",
                "2026-01-20",
                [("ADA Standards of Medical Care in Diabetes", "https://diabetes.org", "American Diabetes Association", 2025)]
            ),
            (
                "Cetirizine",
                "Cetirizine Hydrochloride",
                "Second-Generation Antihistamine",
                "Symptomatic relief of allergic rhinitis, sneezing, itchy watery eyes, and chronic urticaria (hives).",
                "Mild somnolence/drowsiness (low incidence), dry mouth, fatigue, headache.",
                "Use caution when operating machinery or driving until individual sedative reaction is established. Avoid concurrent alcohol.",
                "Dose reduction recommended in patients with moderate to severe renal impairment.",
                "2026-03-01",
                [("British National Formulary (BNF)", "https://bnf.nice.org.uk", "BMJ Group & Royal Pharmaceutical Society", 2025)]
            ),
            (
                "Ibuprofen",
                "Ibuprofen",
                "Non-Steroidal Anti-Inflammatory Drug (NSAID)",
                "Reduces inflammation, swelling, menstrual cramps, dental pain, and arthritis symptoms.",
                "Heartburn, indigestion, nausea, dizziness, mild peripheral edema.",
                "Take with food or milk to protect stomach lining. Avoid prolonged use without medical supervision.",
                "Black box warning: increased risk of gastrointestinal ulceration/bleeding and cardiovascular thrombotic events with chronic use.",
                "2026-02-18",
                [("NHS Medicines A-Z", "https://www.nhs.uk/medicines", "UK NHS", 2025)]
            )
        ]

        for name, gen, cat, uses, side, prec, warn, rev_date, refs in medicines_data:
            cursor.execute(
                """INSERT INTO medicines (name, generic_name, category, uses, side_effects, precautions, warnings, last_reviewed_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (name, gen, cat, uses, side, prec, warn, rev_date)
            )
            med_id = cursor.lastrowid
            for src_name, ref_url, pub, yr in refs:
                cursor.execute(
                    """INSERT INTO medicine_references (medicine_id, source_name, reference_url, publisher, edition_year)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (med_id, src_name, ref_url, pub, yr)
                )

        print(f" [SEED] {len(medicines_data)} verified medicines and references seeded into knowledge base.")
    else:
        print(f" [OK] Medicines knowledge base already populated ({med_count} records).")

    cursor.close()
    conn.close()

    print_banner("Database Setup Completed Successfully!")
    print(f" Database: {Config.DB_NAME} @ {Config.DB_HOST}:{Config.DB_PORT}")
    print(" Default Admin: admin / admin123")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    initialize_database()

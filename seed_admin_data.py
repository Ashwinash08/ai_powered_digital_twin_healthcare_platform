import sqlite3
import os

DATABASE = 'database.db'

def seed_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 1. Update doctor_profiles table if is_approved doesn't exist
    try:
        cursor.execute("ALTER TABLE doctor_profiles ADD COLUMN is_approved INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass # Already exists
        
    # 2. Update ml_models table with precision, recall, f1_score, framework, latency_ms
    for col, col_type in [
        ('framework', 'TEXT DEFAULT "PyTorch"'),
        ('precision', 'REAL DEFAULT 94.0'),
        ('recall', 'REAL DEFAULT 93.5'),
        ('f1_score', 'REAL DEFAULT 93.7'),
        ('latency_ms', 'INTEGER DEFAULT 45')
    ]:
        try:
            cursor.execute(f"ALTER TABLE ml_models ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass

    # 3. Update rag_documents table with chunks_count, file_type
    for col, col_type in [
        ('chunks_count', 'INTEGER DEFAULT 1200'),
        ('file_type', 'TEXT DEFAULT "PDF"')
    ]:
        try:
            cursor.execute(f"ALTER TABLE rag_documents ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass

    # 4. Update ai_agents table with latency_ms, invocations, model_backbone
    for col, col_type in [
        ('latency_ms', 'INTEGER DEFAULT 120'),
        ('invocations', 'INTEGER DEFAULT 1540'),
        ('model_backbone', 'TEXT DEFAULT "GPT-4o / Claude 3.5 Sonnet"')
    ]:
        try:
            cursor.execute(f"ALTER TABLE ai_agents ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass

    # 5. Update patient_profiles table with data_sources, last_synced
    for col, col_type in [
        ('data_sources', 'TEXT DEFAULT "Wearables, EHR, Labs, Manual"'),
        ('last_synced', 'TIMESTAMP')
    ]:
        try:
            cursor.execute(f"ALTER TABLE patient_profiles ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass

    # 5b. Ensure prescriptions table exists and has all columns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        rx_number TEXT UNIQUE NOT NULL,
        medication_name TEXT NOT NULL,
        generic_name TEXT,
        dosage TEXT NOT NULL,
        dosage_form TEXT DEFAULT 'Tablet',
        route TEXT DEFAULT 'Oral',
        frequency TEXT NOT NULL,
        schedule_timing TEXT DEFAULT 'Morning',
        instructions TEXT,
        refill_count INTEGER DEFAULT 3,
        refills_remaining INTEGER DEFAULT 3,
        status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'dispensed', 'pending_verification', 'discontinued')),
        verification_status TEXT DEFAULT 'verified' CHECK(verification_status IN ('verified', 'flagged', 'pending')),
        verification_signature TEXT,
        twin_impact_score INTEGER DEFAULT 4,
        start_date DATE DEFAULT CURRENT_DATE,
        end_date DATE,
        discontinue_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES users(id),
        FOREIGN KEY (doctor_id) REFERENCES users(id)
    )
    """)

    for col, col_type in [
        ('rx_number', 'TEXT DEFAULT "RX-2026-00001"'),
        ('medication_name', 'TEXT DEFAULT "Lisinopril"'),
        ('generic_name', 'TEXT DEFAULT "Lisinopril USP"'),
        ('dosage', 'TEXT DEFAULT "10mg"'),
        ('dosage_form', 'TEXT DEFAULT "Tablet"'),
        ('route', 'TEXT DEFAULT "Oral"'),
        ('frequency', 'TEXT DEFAULT "Once Daily"'),
        ('schedule_timing', 'TEXT DEFAULT "Morning (08:00 AM)"'),
        ('instructions', 'TEXT DEFAULT "Take with water."'),
        ('refill_count', 'INTEGER DEFAULT 3'),
        ('refills_remaining', 'INTEGER DEFAULT 3'),
        ('status', 'TEXT DEFAULT "active"'),
        ('verification_status', 'TEXT DEFAULT "verified"'),
        ('verification_signature', 'TEXT DEFAULT "SIG-VERIFIED"'),
        ('twin_impact_score', 'INTEGER DEFAULT 4'),
        ('start_date', 'DATE DEFAULT CURRENT_DATE'),
        ('end_date', 'DATE'),
        ('discontinue_reason', 'TEXT')
    ]:
        try:
            cursor.execute(f"ALTER TABLE prescriptions ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass

    # Seed ai_agents if empty
    agent_count = cursor.execute("SELECT COUNT(*) FROM ai_agents").fetchone()[0]
    if agent_count == 0:
        agents = [
            ("Diagnosis Agent", "Rule & Bayesian Differential Diagnosis engine analyzing multi-modal symptom vectors", "active", 97.8, 145, 3420, "ClinicalBERT + GPT-4o"),
            ("Prediction & Trajectory Agent", "Bi-LSTM Deep Learning Forecaster for organ health trajectory & degradation", "active", 94.5, 210, 2890, "Bi-LSTM Neural Engine"),
            ("Risk Assessment Agent", "XGBoost Cardiovascular & Metabolic Multi-Factor Stratification Engine", "active", 98.2, 85, 4120, "XGBoost Ensemble v2.3"),
            ("Treatment Consensus Agent", "Clinical Decision Support agent verifying guideline consensus & drug-drug contraindications", "active", 99.1, 190, 2980, "DDI Graph Neural Net"),
            ("Real-Time Monitoring Agent", "Continuous IoT wearable stream processor detecting arrhythmia and BP spikes", "active", 96.4, 45, 12580, "Edge Stream AI Filter"),
            ("Medical Research Agent", "RAG-powered biomedical synthesizer extracting PubMed & ClinicalTrials evidence", "active", 95.0, 320, 1840, "PubMedBERT + Vector RAG"),
            ("Explainable AI (XAI) Agent", "SHAP/LIME Feature attribution and natural language clinician rationale generator", "active", 96.9, 160, 2150, "TreeSHAP Engine v1.2")
        ]
        cursor.executemany("""
            INSERT INTO ai_agents (name, description, status, success_rate, latency_ms, invocations, model_backbone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, agents)

    # Seed ml_models if empty
    model_count = cursor.execute("SELECT COUNT(*) FROM ml_models").fetchone()[0]
    if model_count == 0:
        models = [
            ("Cardiovascular Risk Classifier", "2.3.0", "deployed", 95.4, 96.1, 94.8, 95.4, "XGBoost", 35),
            ("Organ Trajectory Forecaster", "1.4.2", "deployed", 92.8, 93.4, 92.1, 92.7, "PyTorch Bi-LSTM", 180),
            ("Clinical Scribe & Entity Extractor", "3.1.0", "deployed", 96.1, 97.0, 95.2, 96.1, "HuggingFace Transformers", 240),
            ("Drug-Drug Interaction Neural Net", "2.0.0", "deployed", 94.7, 95.5, 93.9, 94.7, "PyTorch Geometric (GNN)", 65),
            ("Hypertension Early Warning System", "1.0.0-beta", "training", 89.4, 90.2, 88.6, 89.4, "TensorFlow / Keras", 110),
            ("Metabolic Syndrome Predictor", "1.1.0", "archived", 88.2, 87.5, 89.0, 88.2, "Scikit-Learn Random Forest", 25)
        ]
        cursor.executemany("""
            INSERT INTO ml_models (name, version, status, accuracy, precision, recall, f1_score, framework, latency_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, models)

    # Seed rag_documents if empty
    rag_count = cursor.execute("SELECT COUNT(*) FROM rag_documents").fetchone()[0]
    if rag_count == 0:
        docs = [
            ("ACC/AHA 2024 Guidelines for Hypertension & Heart Failure", "Cardiology", "indexed", 1840, "PDF Clinical Guideline"),
            ("ADA Standards of Medical Care in Diabetes 2024", "Endocrinology", "indexed", 2450, "PDF Standard Protocol"),
            ("Global Initiative for Chronic Obstructive Lung Disease (GOLD 2024)", "Pulmonology", "indexed", 1230, "PDF Guideline"),
            ("FDA Guidance on Drug-Drug Interactions & Pharmacogenomics", "Pharmacology", "indexed", 3120, "PDF Regulatory Framework"),
            ("ESC Practice Guidelines for Management of Dyslipidaemia", "Cardiology", "indexed", 1680, "PDF Clinical Guideline"),
            ("WHO Digital Health Interventions & AI Ethics Guidelines", "Clinical Protocols", "indexed", 950, "PDF Policy Document")
        ]
        cursor.executemany("""
            INSERT INTO rag_documents (title, category, status, chunks_count, file_type)
            VALUES (?, ?, ?, ?, ?)
        """, docs)

    # Seed alert_rules if empty
    rule_count = cursor.execute("SELECT COUNT(*) FROM alert_rules").fetchone()[0]
    if rule_count == 0:
        rules = [
            ("Critical Heart Rate Spike", "heart_rate > 130 OR heart_rate < 45", "critical", 1),
            ("Severe Hypertensive Crisis", "systolic_bp >= 180 OR diastolic_bp >= 120", "critical", 1),
            ("Cardiac Risk Trajectory Warning", "predicted_cardiac_risk > 0.75", "high", 1),
            ("Digital Twin Inactivity Alert", "last_synced > 48 hours", "medium", 1),
            ("Medication Non-Adherence", "missed_doses >= 3", "medium", 1)
        ]
        cursor.executemany("""
            INSERT INTO alert_rules (rule_name, condition, priority, is_active)
            VALUES (?, ?, ?, ?)
        """, rules)

    # Ensure baseline doctor and patient users exist
    from werkzeug.security import generate_password_hash
    pwd_hash = generate_password_hash("password123")

    existing_doc = cursor.execute("SELECT id FROM users WHERE role = 'doctor'").fetchone()
    if not existing_doc:
        cursor.execute("INSERT OR IGNORE INTO users (name, email, password, role) VALUES ('Dr. Robert Evans', 'doctor@hospital.com', ?, 'doctor')", (pwd_hash,))
        doc_id = cursor.lastrowid
        cursor.execute("INSERT OR IGNORE INTO doctor_profiles (user_id, specialization, license_number, contact_number, is_approved) VALUES (?, 'Cardiology & AI Diagnostics', 'MED-CA-98421', '+1 (555) 234-5678', 1)", (doc_id,))

    existing_pt = cursor.execute("SELECT id FROM users WHERE role = 'patient'").fetchone()
    if not existing_pt:
        cursor.execute("INSERT OR IGNORE INTO users (name, email, password, role) VALUES ('Alex Taylor', 'alex.taylor@gmail.com', ?, 'patient')", (pwd_hash,))
        pt_id1 = cursor.lastrowid
        cursor.execute("""
            INSERT OR IGNORE INTO patient_profiles (user_id, dob, gender, blood_group, medical_history, allergies, current_medications, data_sources, last_synced)
            VALUES (?, '1990-05-14', 'Male', 'O+', 'Pre-hypertension (under active monitoring), laparoscopic appendectomy in 2021.', 'Penicillin (Severe), Latex (Moderate)', 'Lisinopril 10mg daily, Atorvastatin 20mg nightly', 'Wearables, EHR, Labs, Manual', datetime('now', '-10 minutes'))
        """, (pt_id1,))
        cursor.execute("INSERT INTO health_metrics (user_id, heart_rate, blood_pressure, weight, temperature, recorded_at) VALUES (?, 74, '124/80', 81.5, 98.6, datetime('now', '-1 hours'))", (pt_id1,))

        cursor.execute("INSERT OR IGNORE INTO users (name, email, password, role) VALUES ('Maria Santos', 'maria.santos@gmail.com', ?, 'patient')", (pwd_hash,))
        pt_id2 = cursor.lastrowid
        cursor.execute("""
            INSERT OR IGNORE INTO patient_profiles (user_id, dob, gender, blood_group, medical_history, allergies, current_medications, data_sources, last_synced)
            VALUES (?, '1985-11-20', 'Female', 'A+', 'Mild type-2 diabetes mellitus managed with Metformin, stable glycemic control.', 'Sulfa Drugs', 'Metformin 500mg BID', 'Wearables, EHR, Labs', datetime('now', '-2 hours'))
        """, (pt_id2,))
        cursor.execute("INSERT INTO health_metrics (user_id, heart_rate, blood_pressure, weight, temperature, recorded_at) VALUES (?, 68, '118/76', 64.0, 98.4, datetime('now', '-2 hours'))", (pt_id2,))

    # Ensure all doctor profiles are approved
    doctor_users = cursor.execute("SELECT id FROM users WHERE role = 'doctor'").fetchall()
    for doc in doctor_users:
        cursor.execute("INSERT OR IGNORE INTO doctor_profiles (user_id, specialization, license_number, contact_number, is_approved) VALUES (?, 'Cardiology & AI Diagnostics', 'MED-CA-98421', '+1 (555) 234-5678', 1)", (doc[0],))
        cursor.execute("UPDATE doctor_profiles SET is_approved = 1 WHERE user_id = ?", (doc[0],))

    # 6. Create Security & Governance Tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS access_anomalies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        target_patient_id INTEGER,
        anomaly_type TEXT NOT NULL,
        severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
        anomaly_score REAL,
        description TEXT,
        status TEXT DEFAULT 'flagged' CHECK(status IN ('flagged', 'investigating', 'resolved', 'dismissed')),
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (target_patient_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_access_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        urgency_level TEXT DEFAULT 'critical' CHECK(urgency_level IN ('high', 'critical', 'life_threatening')),
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        ip_address TEXT,
        notes TEXT,
        FOREIGN KEY (doctor_id) REFERENCES users(id),
        FOREIGN KEY (patient_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_risk_profiles (
        user_id INTEGER PRIMARY KEY,
        risk_score INTEGER DEFAULT 12,
        risk_level TEXT DEFAULT 'low' CHECK(risk_level IN ('low', 'moderate', 'high', 'critical')),
        anomalies_count INTEGER DEFAULT 0,
        break_glass_count INTEGER DEFAULT 0,
        off_hours_accesses INTEGER DEFAULT 0,
        last_evaluated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status_action TEXT DEFAULT 'normal' CHECK(status_action IN ('normal', 'monitored', 'restricted', 'quarantined')),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Seed access anomalies if empty
    anomaly_count = cursor.execute("SELECT COUNT(*) FROM access_anomalies").fetchone()[0]
    all_users = cursor.execute("SELECT id, role FROM users").fetchall()
    patient_ids = [u[0] for u in all_users if u[1] == 'patient']
    doctor_ids = [u[0] for u in all_users if u[1] == 'doctor']
    admin_ids = [u[0] for u in all_users if u[1] == 'admin']

    sample_doc_id = doctor_ids[0] if doctor_ids else (admin_ids[0] if admin_ids else 1)
    sample_pt_id = patient_ids[0] if patient_ids else 1

    if anomaly_count == 0:
        anomalies = [
            (sample_doc_id, sample_pt_id, "RAPID_BURST_QUERY", "medium", 68.5, "Clinician queried 7 distinct EHR records within 45 seconds during off-shift window.", "flagged"),
            (sample_doc_id, sample_pt_id, "OFF_HOURS_PHI_ACCESS", "low", 42.0, "Patient medical history read outside standard clinic hours (02:14 AM).", "investigating"),
            (sample_doc_id, sample_pt_id, "CROSS_DEPARTMENT_RECORD_ACCESS", "high", 84.0, "Cardiologist accessed oncology biopsy files without active consultation assignment.", "flagged")
        ]
        cursor.executemany("""
            INSERT INTO access_anomalies (user_id, target_patient_id, anomaly_type, severity, anomaly_score, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, anomalies)

    # Seed emergency break-glass sessions if empty
    emerg_count = cursor.execute("SELECT COUNT(*) FROM emergency_access_sessions").fetchone()[0]
    if emerg_count == 0 and doctor_ids and patient_ids:
        cursor.execute("""
            INSERT INTO emergency_access_sessions (doctor_id, patient_id, reason, urgency_level, started_at, expires_at, is_active, ip_address, notes)
            VALUES (?, ?, 'Acute Anaphylactic Shock & Respiratory Arrest in Trauma Bay', 'life_threatening', datetime('now', '-2 hours'), datetime('now', '-1 hours'), 0, '192.168.1.142', 'Immediate epinephrine and intubation protocol required unmasked allergy records.')
        """, (sample_doc_id, sample_pt_id))

    # Initialize user risk profiles for all existing users
    for u in all_users:
        u_id, u_role = u[0], u[1]
        exists = cursor.execute("SELECT user_id FROM user_risk_profiles WHERE user_id = ?", (u_id,)).fetchone()
        if not exists:
            base_score = 14 if u_role == 'doctor' else (5 if u_role == 'patient' else 8)
            cursor.execute("""
                INSERT INTO user_risk_profiles (user_id, risk_score, risk_level, anomalies_count, break_glass_count, off_hours_accesses, status_action)
                VALUES (?, ?, 'low', 0, 0, 0, 'normal')
            """, (u_id, base_score))

    # 7. Create Digital Twin Intelligence & Lifecycle Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS twin_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        version_label TEXT NOT NULL,
        health_score INTEGER DEFAULT 80,
        sync_score REAL DEFAULT 95.0,
        data_quality_score REAL DEFAULT 90.0,
        vitals_snapshot TEXT,
        clinical_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS twin_drift_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        parameter TEXT NOT NULL,
        real_value REAL NOT NULL,
        predicted_value REAL NOT NULL,
        drift_percentage REAL NOT NULL,
        severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
        description TEXT,
        status TEXT DEFAULT 'flagged' CHECK(status IN ('flagged', 'investigating', 'resolved', 'dismissed')),
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS whatif_scenarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        created_by_id INTEGER,
        scenario_title TEXT NOT NULL,
        intervention_type TEXT DEFAULT 'combined',
        parameters_json TEXT,
        projected_health_score INTEGER,
        risk_delta TEXT,
        outcome_summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES users(id),
        FOREIGN KEY (created_by_id) REFERENCES users(id)
    )
    """)

    # Seed twin versions if empty
    version_count = cursor.execute("SELECT COUNT(*) FROM twin_versions").fetchone()[0]
    if version_count == 0 and patient_ids:
        for pid in patient_ids:
            cursor.execute("""
                INSERT INTO twin_versions (patient_id, version_label, health_score, sync_score, data_quality_score, vitals_snapshot, clinical_notes, created_at)
                VALUES (?, 'v1.0.0-Baseline', 72, 91.5, 84.0, '{"heart_rate": 78, "systolic_bp": 138, "diastolic_bp": 88, "weight": 83.5, "glucose": 105}', 'Initial clinical digital twin model calibrated from EHR and wearable baseline intake.', datetime('now', '-30 days'))
            """, (pid,))
            cursor.execute("""
                INSERT INTO twin_versions (patient_id, version_label, health_score, sync_score, data_quality_score, vitals_snapshot, clinical_notes, created_at)
                VALUES (?, 'v1.1.0-Post-Rx', 78, 96.0, 92.5, '{"heart_rate": 74, "systolic_bp": 128, "diastolic_bp": 82, "weight": 82.0, "glucose": 96}', 'Digital twin recalibrated following 4-week Lisinopril 10mg initiation & DASH dietary compliance.', datetime('now', '-7 days'))
            """, (pid,))
            cursor.execute("""
                INSERT INTO twin_versions (patient_id, version_label, health_score, sync_score, data_quality_score, vitals_snapshot, clinical_notes, created_at)
                VALUES (?, 'v1.2.0-Live-Telemetry', 82, 98.4, 95.0, '{"heart_rate": 72, "systolic_bp": 124, "diastolic_bp": 80, "weight": 81.4, "glucose": 94}', 'Current active twin model synchronized with high-frequency continuous wearable stream.', datetime('now', '-1 hours'))
            """, (pid,))

    # Seed twin drift logs if empty
    drift_count = cursor.execute("SELECT COUNT(*) FROM twin_drift_logs").fetchone()[0]
    if drift_count == 0 and patient_ids:
        sample_p = patient_ids[0]
        drifts = [
            (sample_p, "Systolic Blood Pressure (Resting)", 134.0, 122.0, 9.8, "medium", "Real wearable evening systolic BP is 9.8% higher than projected by Bi-LSTM trajectory.", "flagged"),
            (sample_p, "Heart Rate Variability (SDNN)", 38.0, 48.0, -20.8, "high", "Significant reduction in autonomic vagal tone detected vs simulated baseline.", "investigating")
        ]
        cursor.executemany("""
            INSERT INTO twin_drift_logs (patient_id, parameter, real_value, predicted_value, drift_percentage, severity, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, drifts)

    # Seed what-if scenarios if empty
    scenario_count = cursor.execute("SELECT COUNT(*) FROM whatif_scenarios").fetchone()[0]
    if scenario_count == 0 and patient_ids:
        sample_p = patient_ids[0]
        scenarios = [
            (sample_p, 1, "Optimal Cardio Protocol: Lisinopril 20mg + Supervised Zone-2 Exercise", "combined", '{"med_dose": "20mg", "exercise_min": 150, "sodium_limit": "2000mg"}', 88, "-24% 10-Yr CVD Risk", "Model projects systolic normalization to 118 mmHg with sustained reduction in left-ventricular strain index."),
            (sample_p, 1, "Stress Test: Abrupt Antihypertensive Discontinuation", "pharmacological", '{"med_dose": "0mg", "stress_factor": "high"}', 54, "+38% Hypertensive Crisis Risk", "Twin simulation warns of rebound hypertension (projected 156/98 mmHg) within 14 days.")
        ]
        cursor.executemany("""
            INSERT INTO whatif_scenarios (patient_id, created_by_id, scenario_title, intervention_type, parameters_json, projected_health_score, risk_delta, outcome_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, scenarios)

    # 8. Create Pharmacy Module Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        rx_number TEXT UNIQUE NOT NULL,
        medication_name TEXT NOT NULL,
        generic_name TEXT,
        dosage TEXT NOT NULL,
        dosage_form TEXT DEFAULT 'Tablet',
        route TEXT DEFAULT 'Oral',
        frequency TEXT NOT NULL,
        schedule_timing TEXT DEFAULT 'Morning',
        instructions TEXT,
        refill_count INTEGER DEFAULT 3,
        refills_remaining INTEGER DEFAULT 3,
        status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'dispensed', 'pending_verification', 'discontinued')),
        verification_status TEXT DEFAULT 'verified' CHECK(verification_status IN ('verified', 'flagged', 'pending')),
        verification_signature TEXT,
        twin_impact_score INTEGER DEFAULT 4,
        start_date DATE DEFAULT CURRENT_DATE,
        end_date DATE,
        discontinue_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES users(id),
        FOREIGN KEY (doctor_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pharmacy_inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medication_name TEXT NOT NULL,
        generic_name TEXT NOT NULL,
        category TEXT NOT NULL,
        ndc_code TEXT UNIQUE NOT NULL,
        dosage_strength TEXT NOT NULL,
        dosage_form TEXT DEFAULT 'Tablet',
        stock_quantity INTEGER DEFAULT 100,
        min_threshold INTEGER DEFAULT 20,
        unit_price REAL DEFAULT 15.00,
        copay_amount REAL DEFAULT 5.00,
        manufacturer TEXT,
        batch_number TEXT,
        expiry_date DATE,
        status TEXT DEFAULT 'in_stock' CHECK(status IN ('in_stock', 'low_stock', 'out_of_stock')),
        location_shelf TEXT DEFAULT 'Aisle 3 - Bay B',
        substitute_medication TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medication_adherence_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        prescription_id INTEGER NOT NULL,
        medication_name TEXT NOT NULL,
        scheduled_slot TEXT NOT NULL,
        scheduled_time TEXT,
        actual_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'taken' CHECK(status IN ('taken', 'missed', 'skipped', 'snoozed')),
        adherence_date DATE DEFAULT CURRENT_DATE,
        twin_score_delta INTEGER DEFAULT 1,
        notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES users(id),
        FOREIGN KEY (prescription_id) REFERENCES prescriptions(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medication_warnings_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        prescription_id INTEGER,
        warning_type TEXT NOT NULL,
        severity TEXT CHECK(severity IN ('critical', 'high', 'medium', 'low', 'info')),
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        recommendation TEXT NOT NULL,
        detected_by_agent TEXT DEFAULT 'Pharmacology AI Guardian',
        is_acknowledged BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES users(id),
        FOREIGN KEY (prescription_id) REFERENCES prescriptions(id)
    )
    """)

    # Seed Pharmacology Agent if missing
    pharm_agent = cursor.execute("SELECT id FROM ai_agents WHERE name LIKE '%Pharmacology%'").fetchone()
    if not pharm_agent:
        cursor.execute("""
            INSERT INTO ai_agents (name, description, status, success_rate, latency_ms, invocations, model_backbone)
            VALUES ('Pharmacology & Rx Guardian Agent', 'Real-time DDI graph contraindication validator, chronotherapy scheduler, and Digital Twin pharmacogenomics engine', 'active', 99.4, 65, 3810, 'GraphSAGE + BioMedBERT')
        """)

    # Seed Pharmacy Inventory if empty
    inv_count = cursor.execute("SELECT COUNT(*) FROM pharmacy_inventory").fetchone()[0]
    if inv_count == 0:
        inventory_items = [
            ("Lisinopril", "Lisinopril USP", "Cardiovascular", "NDC 68180-514-01", "10mg", "Tablet", 450, 50, 14.50, 4.00, "Lupin Pharmaceuticals", "BCH-2026-8819", "2027-11-30", "in_stock", "Aisle 1 - Bay A (Cardio)", "Enalapril 10mg / Losartan 50mg"),
            ("Atorvastatin", "Atorvastatin Calcium", "Cardiovascular / Lipid", "NDC 00093-7201-01", "20mg", "Film-Coated Tablet", 320, 40, 22.00, 5.00, "Teva Pharmaceuticals", "BCH-2026-9042", "2028-03-15", "in_stock", "Aisle 1 - Bay B (Lipids)", "Rosuvastatin 10mg / Simvastatin 20mg"),
            ("Metformin HCl", "Metformin Hydrochloride", "Antidiabetic / Endocrine", "NDC 50090-2134-0", "500mg", "Extended Release Tab", 580, 60, 12.00, 3.50, "Aurobindo Pharma", "BCH-2026-7731", "2027-09-20", "in_stock", "Aisle 2 - Bay A (Endocrine)", "Empagliflozin 10mg / Glipizide 5mg"),
            ("Spironolactone", "Spironolactone", "Cardiovascular / Diuretic", "NDC 00378-0215-01", "25mg", "Tablet", 18, 25, 18.75, 6.00, "Mylan Specialty", "BCH-2026-4410", "2027-06-18", "low_stock", "Aisle 1 - Bay C (Diuretics)", "Eplerenone 25mg"),
            ("Amoxicillin", "Amoxicillin Trihydrate", "Antibiotic (Beta-Lactam)", "NDC 00781-2613-05", "500mg", "Capsule", 0, 30, 16.20, 5.00, "Sandoz Inc", "BCH-2026-3109", "2026-12-31", "out_of_stock", "Aisle 4 - Bay A (Antibiotics)", "Azithromycin 250mg / Doxycycline 100mg"),
            ("Warfarin Sodium", "Warfarin Sodium", "Anticoagulant", "NDC 00056-0170-70", "5mg", "Scored Tablet", 140, 30, 28.50, 8.00, "Bristol-Myers Squibb", "BCH-2026-6623", "2027-08-14", "in_stock", "Aisle 1 - Bay D (Anticoagulants)", "Apixaban (Eliquis) 5mg"),
            ("Albuterol HFA", "Albuterol Sulfate", "Respiratory / Bronchodilator", "NDC 59310-579-22", "90mcg/actuation", "Inhaler (200 Doses)", 85, 20, 45.00, 10.00, "GlaxoSmithKline", "BCH-2026-1188", "2027-10-05", "in_stock", "Aisle 3 - Bay A (Inhalers)", "Levalbuterol (Xopenex)"),
            ("Omega-3 Acid Ethyl Esters", "Omega-3 Triglycerides", "Cardiovascular / Supplement", "NDC 68180-362-01", "1000mg", "Liquid Softgel", 210, 35, 19.99, 5.00, "NatureMade Medical", "BCH-2026-5541", "2028-01-20", "in_stock", "Aisle 5 - Bay B (Supplements)", "Vascepa (Icosapent ethyl)"),
            ("Amlodipine Besylate", "Amlodipine Besylate", "Cardiovascular / CCB", "NDC 00093-3174-01", "5mg", "Tablet", 390, 45, 11.50, 3.00, "Teva Pharmaceuticals", "BCH-2026-9902", "2027-12-10", "in_stock", "Aisle 1 - Bay A (Cardio)", "Nifedipine ER 30mg / Diltiazem 120mg"),
            ("Ibuprofen", "Ibuprofen USP", "Analgesic / NSAID", "NDC 50090-0012-1", "400mg", "Tablet", 620, 50, 8.50, 2.00, "Perrigo Co", "BCH-2026-2210", "2028-05-15", "in_stock", "Aisle 4 - Bay C (Analgesics)", "Acetaminophen 500mg / Celecoxib 100mg")
        ]
        cursor.executemany("""
            INSERT INTO pharmacy_inventory (medication_name, generic_name, category, ndc_code, dosage_strength, dosage_form, stock_quantity, min_threshold, unit_price, copay_amount, manufacturer, batch_number, expiry_date, status, location_shelf, substitute_medication)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, inventory_items)

    # Seed Sample Prescriptions for all patient accounts
    if patient_ids and doctor_ids:
        doc_id = doctor_ids[0]
        for pid in patient_ids:
            rx_for_pt = cursor.execute("SELECT COUNT(*) FROM prescriptions WHERE patient_id = ?", (pid,)).fetchone()[0]
            if rx_for_pt == 0:
                prescriptions_data = [
                    (pid, doc_id, f"RX-2026-{pid}01", "Lisinopril", "Lisinopril USP", "10mg", "Tablet", "Oral", "Once Daily", "Morning (08:00 AM)", "Take 1 tablet every morning with a full glass of water. Monitor resting BP weekly.", 4, 3, "active", "verified", "SIG-DR-ROBERTEVANS-MD-98421", 5, "2026-01-15", "2026-07-15", None),
                    (pid, doc_id, f"RX-2026-{pid}02", "Atorvastatin", "Atorvastatin Calcium", "20mg", "Film-Coated Tablet", "Oral", "Once Nightly", "Bedtime (10:00 PM)", "Take 1 tablet at bedtime. Avoid concurrent consumption of grapefruit juice.", 3, 2, "active", "verified", "SIG-DR-ROBERTEVANS-MD-98421", 4, "2026-01-15", "2026-07-15", None),
                    (pid, doc_id, f"RX-2026-{pid}03", "Omega-3 Medical Grade", "Omega-3 Ethyl Esters", "1000mg", "Liquid Softgel", "Oral", "Once Daily", "Midday (01:00 PM)", "Take 1 capsule with food at lunch for optimal cardiovascular lipid profile.", 5, 4, "active", "verified", "SIG-DR-ROBERTEVANS-MD-98421", 3, "2026-02-01", "2026-08-01", None),
                    (pid, doc_id, f"RX-2025-{pid}99", "Hydrochlorothiazide", "HCTZ", "12.5mg", "Tablet", "Oral", "Once Daily", "Morning", "Discontinued: Mild electrolyte shift resolved; substituted with DASH diet & Lisinopril titration.", 0, 0, "discontinued", "verified", "SIG-DR-ROBERTEVANS-MD-98421", 2, "2025-06-10", "2025-11-15", "Electrolyte optimization / mild hypokalemia resolved")
                ]
                cursor.executemany("""
                    INSERT INTO prescriptions (patient_id, doctor_id, rx_number, medication_name, generic_name, dosage, dosage_form, route, frequency, schedule_timing, instructions, refill_count, refills_remaining, status, verification_status, verification_signature, twin_impact_score, start_date, end_date, discontinue_reason)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, prescriptions_data)

            # Seed Adherence Logs
            adh_for_pt = cursor.execute("SELECT COUNT(*) FROM medication_adherence_logs WHERE patient_id = ?", (pid,)).fetchone()[0]
            if adh_for_pt == 0:
                rx_rows = cursor.execute("SELECT id, medication_name FROM prescriptions WHERE patient_id = ? AND status = 'active'", (pid,)).fetchall()
                if rx_rows:
                    adherence_seeds = []
                    import datetime
                    today = datetime.date.today()
                    
                    for days_ago in range(6, -1, -1):
                        log_date = str(today - datetime.timedelta(days=days_ago))
                        for rx in rx_rows:
                            rx_id, rx_name = rx[0], rx[1]
                            slot = "Morning" if "Lisinopril" in rx_name else ("Bedtime" if "Atorvastatin" in rx_name else "Midday")
                            sched_time = "08:00 AM" if slot == "Morning" else ("10:00 PM" if slot == "Bedtime" else "01:00 PM")
                            
                            if days_ago == 2 and slot == "Bedtime":
                                status = "missed"
                                notes = "Missed evening dose due to late travel. Logged in Digital Twin."
                                delta = -2
                            elif days_ago == 0 and slot == "Bedtime":
                                status = "snoozed"
                                notes = "Pending evening schedule."
                                delta = 0
                            else:
                                status = "taken"
                                notes = "Verified taken via smart pillbox / mobile reminder."
                                delta = 1
                                
                            adherence_seeds.append((pid, rx_id, rx_name, slot, sched_time, status, log_date, delta, notes))
                    
                    cursor.executemany("""
                        INSERT INTO medication_adherence_logs (patient_id, prescription_id, medication_name, scheduled_slot, scheduled_time, status, adherence_date, twin_score_delta, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, adherence_seeds)

            # Seed Medication Warnings
            warn_for_pt = cursor.execute("SELECT COUNT(*) FROM medication_warnings_log WHERE patient_id = ?", (pid,)).fetchone()[0]
            if warn_for_pt == 0:
                warnings_seed = [
                    (pid, None, "drug_allergy", "critical", "Severe Cross-Reactivity: Penicillin Allergy Warning", "Patient has severe Penicillin allergy documented in Digital Twin. All Beta-lactam antibiotics (Amoxicillin, Ampicillin, Augmentin) are strictly contra-indicated.", "Avoid beta-lactam class. Substitute with Macrolides (Azithromycin) or Fluoroquinolones if antibiotic therapy needed.", "Pharmacology AI Guardian", 0),
                    (pid, None, "drug_drug", "medium", "NSAID Antagonism with ACE Inhibitor (Lisinopril)", "Co-administration of OTC Ibuprofen/Naproxen (NSAIDs) with Lisinopril reduces antihypertensive efficacy and elevates acute renal workload.", "Recommend Acetaminophen 500mg as first-line analgesic to preserve renal filtration and BP stability.", "Pharmacology AI Guardian", 0),
                    (pid, None, "food_interaction", "low", "Chronotherapy & Dietary Optimization: Atorvastatin", "Atorvastatin hepatic HMG-CoA reductase suppression is maximal when taken at bedtime. Grapefruit juice (>250ml) inhibits CYP3A4 metabolism and should be avoided.", "Maintain evening dosing schedule. Avoid large quantities of citrus/grapefruit juice.", "Pharmacology AI Guardian", 1)
                ]
                cursor.executemany("""
                    INSERT INTO medication_warnings_log (patient_id, prescription_id, warning_type, severity, title, description, recommendation, detected_by_agent, is_acknowledged)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, warnings_seed)

    conn.commit()
    conn.close()
    print("Database seeded and migrated successfully with Digital Twin intelligence and Pharmacy tables!")

if __name__ == '__main__':
    seed_database()




CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('doctor', 'patient', 'admin')),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patient_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    dob DATE,
    gender TEXT,
    blood_group TEXT,
    medical_history TEXT,
    allergies TEXT,
    current_medications TEXT,
    data_sources TEXT DEFAULT 'Wearables, EHR, Labs, Manual',
    last_synced TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS patient_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS health_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    heart_rate INTEGER,
    blood_pressure TEXT,
    weight REAL,
    temperature REAL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert a default admin user
-- The password is '1234'
INSERT OR IGNORE INTO users (name, email, password, role) 
VALUES ('System Admin', 'admin@gmail.com', '1234', 'admin');

CREATE TABLE IF NOT EXISTS doctor_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    specialization TEXT,
    license_number TEXT,
    contact_number TEXT,
    is_approved INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS consultations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    notes TEXT,
    prescriptions TEXT,
    follow_up_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES users(id),
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS clinical_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    is_read BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ai_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    prediction_type TEXT NOT NULL,
    result TEXT NOT NULL,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ai_agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active',
    success_rate REAL,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ml_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    status TEXT DEFAULT 'deployed',
    accuracy REAL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rag_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    status TEXT DEFAULT 'indexed',
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alert_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    condition TEXT NOT NULL,
    priority TEXT,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    ip_address TEXT,
    status TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_type TEXT NOT NULL,
    value REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
);

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
);

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
);

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
);

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
);

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
);

CREATE TABLE IF NOT EXISTS patient_emergency_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    emergency_token TEXT UNIQUE NOT NULL,
    blood_group TEXT DEFAULT 'O+',
    is_organ_donor BOOLEAN DEFAULT 1,
    dnr_status BOOLEAN DEFAULT 0,
    implantable_devices TEXT DEFAULT 'None',
    critical_conditions TEXT,
    allergies_critical TEXT,
    current_medications TEXT,
    emergency_contact_1_name TEXT,
    emergency_contact_1_phone TEXT,
    emergency_contact_1_relation TEXT,
    emergency_contact_2_name TEXT,
    emergency_contact_2_phone TEXT,
    emergency_contact_2_relation TEXT,
    primary_physician_name TEXT,
    primary_physician_phone TEXT,
    preferred_hospital TEXT,
    special_emergency_instructions TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS emergency_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    severity_level TEXT DEFAULT 'ESI-2 (Emergent)',
    latitude REAL,
    longitude REAL,
    location_address TEXT,
    ai_triage_summary TEXT,
    ai_countermeasures TEXT,
    dispatched_facility TEXT,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'en_route', 'admitted', 'resolved')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

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
);

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
);

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
);

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
);




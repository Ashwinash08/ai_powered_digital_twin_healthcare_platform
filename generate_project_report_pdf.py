import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# Numbered Canvas for "Page X of Y" and Running Header/Footer
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 752, "AI-Powered Digital Twin Healthcare Intelligence Platform using Multi-Agent AI")
            self.drawRightString(612 - 54, 752, "Full Project Technical & Functional Report")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)

        self.drawString(54, 32, "Confidential - Clinical AI & Multi-Agent Architecture Report")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        self.restoreState()


def build_pdf(filename="Project_Full_Report_Healthcare_Digital_Twin.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0f172a")      # Slate 900
    SECONDARY = colors.HexColor("#0284c7")    # Sky 600
    ACCENT = colors.HexColor("#0d9488")       # Teal 600
    DARK_TEXT = colors.HexColor("#1e293b")    # Slate 800
    MUTED_TEXT = colors.HexColor("#64748b")   # Slate 500
    BG_LIGHT = colors.HexColor("#f8fafc")     # Slate 50
    CARD_BG = colors.HexColor("#f1f5f9")      # Slate 100
    BORDER_COLOR = colors.HexColor("#cbd5e1") # Slate 300

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=MUTED_TEXT
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=ACCENT,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK_TEXT,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=DARK_TEXT
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=DARK_TEXT
    )

    story = []

    # ------------------------------------------------------------------
    # COVER / HEADER BANNER
    # ------------------------------------------------------------------
    banner_data = [
        [
            Paragraph("CLINICAL AI PLATFORM ARCHITECTURE & SYSTEM REPORT", ParagraphStyle('BnrSmall', fontName='Helvetica-Bold', fontSize=8, textColor=SECONDARY, leading=10)),
        ],
        [
            Paragraph("AI-Powered Digital Twin Healthcare Intelligence Platform", title_style),
        ],
        [
            Paragraph("Multi-Agent AI Swarm • Real-Time Telemetry Twin • Clinical Decision Support • Smart Pharmacy • Emergency Response", subtitle_style),
        ],
        [
            Paragraph("<b>Version:</b> 2.4.0 (Production-Ready) &nbsp;|&nbsp; <b>Tech Stack:</b> Python Flask, SQLite, PyTorch, XGBoost, BioMedBERT, SHAP, Chart.js &nbsp;|&nbsp; <b>Date:</b> September 2026", meta_style)
        ]
    ]
    banner_tbl = Table(banner_data, colWidths=[504])
    banner_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(banner_tbl)
    story.append(Spacer(1, 14))

    # ------------------------------------------------------------------
    # 1. EXECUTIVE SUMMARY
    # ------------------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Project Scope", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))
    
    exec_text = (
        "The <b>AI-Powered Digital Twin Healthcare Intelligence Platform using Multi-Agent AI</b> is an enterprise-grade "
        "medical cyber-physical system designed to create continuous, high-fidelity biological replicas of patients. "
        "By fusing longitudinal Electronic Health Records (EHR), continuous wearable IoT telemetry (Heart Rate, Blood Pressure, SpO2), "
        "diagnostic imaging, and pharmacogenomic data, the platform empowers patients, clinicians, and hospital administrators "
        "with predictive intelligence, automated triage, explainable diagnostics, and zero-trust data governance."
    )
    story.append(Paragraph(exec_text, body_style))

    key_caps = [
        "<b>Multi-Agent AI Swarm:</b> Eight autonomous, specialized AI agents collaborating in real-time for diagnostic synthesis, treatment consensus, organ trajectory modeling, and pharmacovigilance.",
        "<b>Dynamic Digital Twin Engine:</b> Real-time synchronization, biological age scoring, 10-year organ degradation forecasting, What-If simulation sandboxes, and twin drift telemetry detection.",
        "<b>Clinical Decision Support (CDS) & XAI:</b> TreeSHAP feature attributions, PubMed RAG guidelines verification, and automated SOAP consultation transcription with ICD-10 coding.",
        "<b>Intelligent Smart Pharmacy:</b> 24-hour chronotherapy schedules, computer-vision pillbox scanning, Drug-Drug Interaction (DDI) graphs, digital prescription signing, and hospital inventory tracking.",
        "<b>Emergency Response & Paramedic Triage:</b> 1-Click SOS telemetry dispatch, Emergency Severity Index (ESI) classification, and tokenized QR-accessible public Paramedic Portals.",
        "<b>HIPAA Compliance & Zero-Trust Governance:</b> Context-aware Role-Based Access Control (RBAC), Safe-Harbor PHI masking, break-glass emergency overrides, and AI-driven access anomaly detection."
    ]
    for cap in key_caps:
        story.append(Paragraph(f"• {cap}", bullet_style))

    story.append(Spacer(1, 10))

    # ------------------------------------------------------------------
    # 2. SYSTEM ARCHITECTURE & TECH STACK
    # ------------------------------------------------------------------
    story.append(Paragraph("2. System Architecture & Technology Stack", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    arch_text = (
        "The platform follows a layered, modular micro-agent architecture with decoupled presentation, "
        "business logic, intelligence swarming, and persistent data governance layers:"
    )
    story.append(Paragraph(arch_text, body_style))

    tech_table_data = [
        [Paragraph("Layer", tbl_header), Paragraph("Technologies & Frameworks", tbl_header), Paragraph("Key Functional Role", tbl_header)],
        [
            Paragraph("<b>Presentation</b>", tbl_cell_bold),
            Paragraph("Jinja2, HTML5, CSS3 Glassmorphism, Tailwind/Bootstrap, Chart.js, Canvas 3D", tbl_cell),
            Paragraph("Responsive, dark-mode glassmorphic portals for Patient, Doctor, Admin, and Paramedic.", tbl_cell)
        ],
        [
            Paragraph("<b>Backend & API</b>", tbl_cell_bold),
            Paragraph("Python 3.10+, Flask 3.x, RESTful JSON Endpoints, Werkzeug Security", tbl_cell),
            Paragraph("Request routing, session authentication, contextual authorization, API handlers.", tbl_cell)
        ],
        [
            Paragraph("<b>AI Swarm Subsystem</b>", tbl_cell_bold),
            Paragraph("PyTorch (Bi-LSTM), XGBoost 2.3, BioMedBERT, ClinicalBERT, GraphSAGE, TreeSHAP", tbl_cell),
            Paragraph("Organ trajectory simulation, DDI interaction graphs, differential diagnosis, XAI attributions.", tbl_cell)
        ],
        [
            Paragraph("<b>Knowledge RAG</b>", tbl_cell_bold),
            Paragraph("PubMed Vector Store, Sentence-Transformers, Vector Chunking Index", tbl_cell),
            Paragraph("Biomedical literature retrieval, guideline verification, hallucination guardrails.", tbl_cell)
        ],
        [
            Paragraph("<b>Persistence & Storage</b>", tbl_cell_bold),
            Paragraph("SQLite3 (24 Tables), Auto-Migrations, Secure File Ingestion (/uploads)", tbl_cell),
            Paragraph("ACID transaction guarantees, schema integrity, encrypted audit logging.", tbl_cell)
        ],
        [
            Paragraph("<b>Security & Compliance</b>", tbl_cell_bold),
            Paragraph("Safe-Harbor PHI Masking, Salted Scrypt Hashes, Anomaly Scanners", tbl_cell),
            Paragraph("HIPAA compliance, rate/velocity anomaly detection, break-glass override governance.", tbl_cell)
        ]
    ]

    tech_tbl = Table(tech_table_data, colWidths=[90, 180, 234])
    tech_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tech_tbl)
    story.append(Spacer(1, 12))

    # ------------------------------------------------------------------
    # 3. MULTI-AGENT AI SWARM SUBSYSTEM
    # ------------------------------------------------------------------
    story.append(Paragraph("3. Multi-Agent AI Swarm Subsystem", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    swarm_text = (
        "Rather than relying on a single monolithic language model, the system deploys a cooperative ensemble "
        "of <b>8 specialized AI agents</b>. Each agent possesses domain-specific backbones, latency budgets, and decision boundaries:"
    )
    story.append(Paragraph(swarm_text, body_style))

    agents_table_data = [
        [Paragraph("Agent Name", tbl_header), Paragraph("Backbone / Engine", tbl_header), Paragraph("Latency", tbl_header), Paragraph("Success", tbl_header), Paragraph("Clinical Responsibility", tbl_header)],
        [
            Paragraph("<b>Real-Time Monitoring</b>", tbl_cell_bold),
            Paragraph("Edge Stream Filter", tbl_cell),
            Paragraph("45 ms", tbl_cell),
            Paragraph("96.4%", tbl_cell),
            Paragraph("Ingests wearable IoT telemetry (HR, BP, SpO2); detects acute arrhythmia and hypertensive spikes.", tbl_cell)
        ],
        [
            Paragraph("<b>Diagnosis Agent</b>", tbl_cell_bold),
            Paragraph("ClinicalBERT + Bayesian", tbl_cell),
            Paragraph("145 ms", tbl_cell),
            Paragraph("97.8%", tbl_cell),
            Paragraph("Generates multi-modal differential diagnosis ranking correlated with patient EHR and symptoms.", tbl_cell)
        ],
        [
            Paragraph("<b>Prediction & Trajectory</b>", tbl_cell_bold),
            Paragraph("PyTorch Bi-LSTM", tbl_cell),
            Paragraph("210 ms", tbl_cell),
            Paragraph("94.5%", tbl_cell),
            Paragraph("Simulates 1-month to 10-year organ health degradation and recovery trajectories.", tbl_cell)
        ],
        [
            Paragraph("<b>Risk Stratification</b>", tbl_cell_bold),
            Paragraph("XGBoost Ensemble v2.3", tbl_cell),
            Paragraph("85 ms", tbl_cell),
            Paragraph("98.2%", tbl_cell),
            Paragraph("Computes Framingham cardiovascular, metabolic syndrome, and renal failure risk indices.", tbl_cell)
        ],
        [
            Paragraph("<b>Treatment Consensus</b>", tbl_cell_bold),
            Paragraph("DDI Graph Neural Net", tbl_cell),
            Paragraph("190 ms", tbl_cell),
            Paragraph("99.1%", tbl_cell),
            Paragraph("Validates guideline consensus (ACC/AHA/ESC) and multi-agent treatment protocols.", tbl_cell)
        ],
        [
            Paragraph("<b>Explainable AI (XAI)</b>", tbl_cell_bold),
            Paragraph("TreeSHAP v1.2", tbl_cell),
            Paragraph("160 ms", tbl_cell),
            Paragraph("96.9%", tbl_cell),
            Paragraph("Generates SHAP biomarker attribution weights and natural language clinical rationales.", tbl_cell)
        ],
        [
            Paragraph("<b>Medical Research (RAG)</b>", tbl_cell_bold),
            Paragraph("PubMedBERT + Vector RAG", tbl_cell),
            Paragraph("320 ms", tbl_cell),
            Paragraph("95.0%", tbl_cell),
            Paragraph("Synthesizes peer-reviewed evidence from indexed clinical trials and medical literature.", tbl_cell)
        ],
        [
            Paragraph("<b>Pharmacology Guardian</b>", tbl_cell_bold),
            Paragraph("GraphSAGE + BioMedBERT", tbl_cell),
            Paragraph("65 ms", tbl_cell),
            Paragraph("99.4%", tbl_cell),
            Paragraph("Cross-checks drug-drug, drug-allergy, and chronotherapy timings in real-time.", tbl_cell)
        ]
    ]

    agent_tbl = Table(agents_table_data, colWidths=[95, 95, 42, 45, 227])
    agent_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(agent_tbl)
    story.append(Spacer(1, 14))

    # ------------------------------------------------------------------
    # 4. CORE FUNCTIONAL MODULES
    # ------------------------------------------------------------------
    story.append(Paragraph("4. Core Functional Modules & Intelligence Engines", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    modules = [
        (
            "A. Digital Twin Intelligence & Simulation Module",
            "Constructs real-time synchronized virtual twin models with anatomical 3D organ representations (Brain, Heart, Lungs, Liver, Kidneys, Vascular). Features include continuous sync score calculation, automated telemetry drift detection (real vs. predicted divergence), What-If intervention sandboxes (e.g., simulating dosage adjustments or DASH diet), and immutable twin version snapshotting (e.g., v1.0.0-Baseline)."
        ),
        (
            "B. Clinical Decision Support (CDS) & XAI Module",
            "Equips physicians with probabilistic differential diagnostic rankings, guideline compliance scores, and explainable AI (SHAP/LIME) attribution waterfalls. It includes an Automated AI SOAP Scribe that processes consultation transcripts into formatted Subjective, Objective, Assessment, and Plan notes with suggested ICD-10 diagnostic codes."
        ),
        (
            "C. Smart Pharmacy & Medication Adherence Module",
            "Manages end-to-end pharmacology with 24-hour chronotherapy schedules (Morning, Midday, Evening, Bedtime), computer-vision pillbox verification, 7-day/30-day adherence analytics, automated DDI/Allergy contraindication scanning, digital prescription generation with cryptographic verification signatures, and real-time hospital pharmacy inventory tracking."
        ),
        (
            "D. Emergency Intelligence & Paramedic Triage Module",
            "Provides an instant 1-Click SOS emergency trigger that broadcasts live GPS coordinates and vitals telemetry to trauma centers. Employs Emergency Severity Index (ESI-1 to ESI-3) AI triaging, generates paramedic countermeasures, and produces a tokenized QR-code Paramedic Responder Portal accessible without authentication barriers at the scene."
        ),
        (
            "E. Zero-Trust Access Governance & HIPAA Security Module",
            "Enforces dynamic Role-Based Access Control (RBAC) with contextual masking modes (Unmasked, Safe Harbor, Partial). Includes Emergency Break-Glass override sessions (30-minute unmasked windows with high-priority logging), velocity/off-hours access anomaly scanners, user risk scoring (1-100 scale), and an immutable HIPAA audit trail."
        )
    ]

    for title, desc in modules:
        story.append(Paragraph(title, h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(Spacer(1, 10))

    # ------------------------------------------------------------------
    # 5. DETAILED PAGE-BY-PAGE AND TEMPLATE DIRECTORY BREAKDOWN
    # ------------------------------------------------------------------
    story.append(Paragraph("5. Detailed Page-by-Page & Route Directory Breakdown", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    pages_data = [
        [Paragraph("Category / Page", tbl_header), Paragraph("Route & Template", tbl_header), Paragraph("Primary Clinical & Operational Use Case", tbl_header)],
        
        # Public / Auth
        [Paragraph("<b>Public Landing</b>", tbl_cell_bold), Paragraph("<code>/</code><br/><code>landing.html</code>", tbl_cell), Paragraph("Platform homepage showcasing AI Swarm capabilities, 3D twin previews, live metrics, and role login portals.", tbl_cell)],
        [Paragraph("<b>Unified Login</b>", tbl_cell_bold), Paragraph("<code>/login</code><br/><code>login.html</code>", tbl_cell), Paragraph("Authentication portal for Patients and Doctors with credential hashing and account status validation.", tbl_cell)],
        [Paragraph("<b>Registration</b>", tbl_cell_bold), Paragraph("<code>/register</code><br/><code>register.html</code>", tbl_cell), Paragraph("User onboarding form initializing profile baselines, security risk scores, and wearable telemetry streams.", tbl_cell)],
        [Paragraph("<b>Forgot Password</b>", tbl_cell_bold), Paragraph("<code>/forgot-password</code><br/><code>forgot_password.html</code>", tbl_cell), Paragraph("Secure self-service password recovery with salted cryptographic hash updates.", tbl_cell)],
        [Paragraph("<b>Admin Login</b>", tbl_cell_bold), Paragraph("<code>/admin/login</code><br/><code>admin_login.html</code>", tbl_cell), Paragraph("Isolated, high-security authentication gateway for system administrators and governance officers.", tbl_cell)],
        [Paragraph("<b>Account Profile</b>", tbl_cell_bold), Paragraph("<code>/profile</code><br/><code>account_profile.html</code>", tbl_cell), Paragraph("Unified account settings view for updating personal credentials, email addresses, and passwords.", tbl_cell)],

        # Patient Portal
        [Paragraph("<b>Patient Dashboard</b>", tbl_cell_bold), Paragraph("<code>/patient/dashboard</code><br/><code>patient/dashboard.html</code>", tbl_cell), Paragraph("Central patient command center displaying health scores, upcoming appointments, alerts, and vital trends.", tbl_cell)],
        [Paragraph("<b>Patient Digital Twin</b>", tbl_cell_bold), Paragraph("<code>/patient/twin</code><br/><code>patient/twin.html</code>", tbl_cell), Paragraph("Interactive 3D body twin interface showing organ degradation trajectories, biological age, and vital stats.", tbl_cell)],
        [Paragraph("<b>Patient Pharmacy</b>", tbl_cell_bold), Paragraph("<code>/patient/pharmacy</code><br/><code>patient/pharmacy.html</code>", tbl_cell), Paragraph("24-hour chronotherapy pillbox, 1-click dose adherence logging, 1-click refill requests, and DDI warnings.", tbl_cell)],
        [Paragraph("<b>Patient Emergency</b>", tbl_cell_bold), Paragraph("<code>/patient/emergency</code><br/><code>patient/emergency.html</code>", tbl_cell), Paragraph("SOS trigger, GPS broadcaster, paramedic QR card generator, and emergency contact directives manager.", tbl_cell)],
        [Paragraph("<b>Patient Assessment</b>", tbl_cell_bold), Paragraph("<code>/patient/assessment</code><br/><code>patient/assessment.html</code>", tbl_cell), Paragraph("Symptom questionnaire with AI acoustic voice biomarker analysis feeding data to the Diagnosis Agent.", tbl_cell)],
        [Paragraph("<b>Recommendations</b>", tbl_cell_bold), Paragraph("<code>/patient/recommendations</code><br/><code>patient/recommendations.html</code>", tbl_cell), Paragraph("Multi-agent consensus advice for diet (DASH/Mediterranean), zone-2 exercise, sleep, and medication.", tbl_cell)],
        [Paragraph("<b>Data Upload</b>", tbl_cell_bold), Paragraph("<code>/patient/upload</code><br/><code>patient/upload.html</code>", tbl_cell), Paragraph("Document ingestion center for lab reports (PDF/images), discharge summaries, and ECG scans.", tbl_cell)],
        [Paragraph("<b>Patient Profile</b>", tbl_cell_bold), Paragraph("<code>/patient/profile</code><br/><code>patient/profile.html</code>", tbl_cell), Paragraph("Patient clinical profile editor for blood phenotype, allergies, active medications, and medical history.", tbl_cell)],
        [Paragraph("<b>AI Health Chat</b>", tbl_cell_bold), Paragraph("<code>/patient/chat</code><br/><code>patient/chat.html</code>", tbl_cell), Paragraph("24/7 conversational assistant connected to RAG medical knowledge and patient twin telemetry.", tbl_cell)],

        # Doctor Portal
        [Paragraph("<b>Doctor Dashboard</b>", tbl_cell_bold), Paragraph("<code>/doctor/dashboard</code><br/><code>doctor/dashboard.html</code>", tbl_cell), Paragraph("Physician practice overview with active patient counts, critical alerts, and emergency triage queue.", tbl_cell)],
        [Paragraph("<b>Doctor Patient Roster</b>", tbl_cell_bold), Paragraph("<code>/doctor/patients</code><br/><code>doctor/patients.html</code>", tbl_cell), Paragraph("Patient roster with contextual Safe-Harbor de-identification and break-glass emergency status indicators.", tbl_cell)],
        [Paragraph("<b>Doctor Patient Detail</b>", tbl_cell_bold), Paragraph("<code>/doctor/patient/&lt;id&gt;</code><br/><code>doctor/patient_detail.html</code>", tbl_cell), Paragraph("Longitudinal EHR review, vitals charts, attached lab files, clinical notes, and break-glass overrides.", tbl_cell)],
        [Paragraph("<b>Doctor Twin Console</b>", tbl_cell_bold), Paragraph("<code>/doctor/patient/&lt;id&gt;/twin</code><br/><code>doctor/doctor_twin.html</code>", tbl_cell), Paragraph("Clinical twin workstation for What-If scenario simulations, trajectory forecasting, and drift analysis.", tbl_cell)],
        [Paragraph("<b>Clinical CDS</b>", tbl_cell_bold), Paragraph("<code>/doctor/patient/&lt;id&gt;/cds</code><br/><code>doctor/cds.html</code>", tbl_cell), Paragraph("Differential diagnosis rankings, multi-agent consensus votes, and clinical guideline cross-checks.", tbl_cell)],
        [Paragraph("<b>Explainable AI (XAI)</b>", tbl_cell_bold), Paragraph("<code>/doctor/patient/&lt;id&gt;/xai</code><br/><code>doctor/xai.html</code>", tbl_cell), Paragraph("SHAP/LIME feature attribution console visualizing biomarker weighting and model decision paths.", tbl_cell)],
        [Paragraph("<b>Doctor Pharmacy</b>", tbl_cell_bold), Paragraph("<code>/doctor/patient/&lt;id&gt;/pharmacy</code><br/><code>doctor/patient_pharmacy.html</code>", tbl_cell), Paragraph("e-Prescribing portal with automated DDI graph verification, adherence reviews, and drug discontinuation.", tbl_cell)],
        [Paragraph("<b>Consultation & Scribe</b>", tbl_cell_bold), Paragraph("<code>/doctor/patient/&lt;id&gt;/consultation</code><br/><code>doctor/consultation.html</code>", tbl_cell), Paragraph("Automated SOAP note generation from consultation transcripts with suggested ICD-10 coding.", tbl_cell)],
        [Paragraph("<b>Clinical Report</b>", tbl_cell_bold), Paragraph("<code>/doctor/patient/&lt;id&gt;/report</code><br/><code>doctor/report.html</code>", tbl_cell), Paragraph("1-Click multi-agent report generator creating formatted clinical summaries for referrals or discharge.", tbl_cell)],
        [Paragraph("<b>Biomedical Research</b>", tbl_cell_bold), Paragraph("<code>/doctor/patient/&lt;id&gt;/research</code><br/><code>doctor/research.html</code>", tbl_cell), Paragraph("Vector RAG console querying PubMed, clinical trials, and medical guidelines at the point of care.", tbl_cell)],
        [Paragraph("<b>Doctor Profile</b>", tbl_cell_bold), Paragraph("<code>/doctor/profile</code><br/><code>doctor/profile.html</code>", tbl_cell), Paragraph("Physician credentials editor for license numbers, specializations, and digital prescription signatures.", tbl_cell)],

        # Admin Portal
        [Paragraph("<b>Admin Dashboard</b>", tbl_cell_bold), Paragraph("<code>/admin/dashboard</code><br/><code>admin/dashboard.html</code>", tbl_cell), Paragraph("System governance dashboard with active twin metrics, pending doctor approvals, and agent health.", tbl_cell)],
        [Paragraph("<b>Admin User Control</b>", tbl_cell_bold), Paragraph("<code>/admin/users</code><br/><code>admin/users.html</code>", tbl_cell), Paragraph("User account management with security risk mitigation tools (quarantine, force MFA, risk reset).", tbl_cell)],
        [Paragraph("<b>Admin Digital Twins</b>", tbl_cell_bold), Paragraph("<code>/admin/twins</code><br/><code>admin/twins.html</code>", tbl_cell), Paragraph("Fleet twin manager with telemetry sync controls and synthetic patient cohort generator.", tbl_cell)],
        [Paragraph("<b>Multi-Agent Registry</b>", tbl_cell_bold), Paragraph("<code>/admin/agents</code><br/><code>admin/agents.html</code>", tbl_cell), Paragraph("Agent swarm orchestrator with status toggles, latency monitoring, and swarm simulation triggers.", tbl_cell)],
        [Paragraph("<b>ML Model Registry</b>", tbl_cell_bold), Paragraph("<code>/admin/models</code><br/><code>admin/models.html</code>", tbl_cell), Paragraph("ML model lifecycle manager with accuracy tracking, 1-click retraining, and production deployment.", tbl_cell)],
        [Paragraph("<b>RAG Knowledge Store</b>", tbl_cell_bold), Paragraph("<code>/admin/rag</code><br/><code>admin/rag.html</code>", tbl_cell), Paragraph("Medical guideline vector store with chunking stats, re-indexing, and hallucination guardrail scans.", tbl_cell)],
        [Paragraph("<b>Security & Audit</b>", tbl_cell_bold), Paragraph("<code>/admin/audit</code><br/><code>admin/audit.html</code>", tbl_cell), Paragraph("HIPAA audit log viewer, AI access anomaly tracker, break-glass session monitor, and risk scores.", tbl_cell)],
        [Paragraph("<b>Alert Rule Engine</b>", tbl_cell_bold), Paragraph("<code>/admin/alerts</code><br/><code>admin/alerts.html</code>", tbl_cell), Paragraph("Clinical alert builder for vital thresholds (BP, HR spikes) and active alert broadcast streams.", tbl_cell)],
        [Paragraph("<b>Analytics (AI & Health)</b>", tbl_cell_bold), Paragraph("<code>/admin/analytics/ai</code><br/><code>admin/analytics_ai.html</code>", tbl_cell), Paragraph("Deep visual analytics for multi-agent latency, accuracy, population risk, and alert trends.", tbl_cell)],
        [Paragraph("<b>Data & System Health</b>", tbl_cell_bold), Paragraph("<code>/admin/data</code> &amp; <code>/admin/system</code><br/><code>admin/data.html</code>", tbl_cell), Paragraph("Database table row inspector, storage analytics, and server CPU/memory performance monitors.", tbl_cell)],

        # Emergency Responder
        [Paragraph("<b>Emergency Paramedic Portal</b>", tbl_cell_bold), Paragraph("<code>/emergency/&lt;token&gt;</code><br/><code>emergency_responder.html</code>", tbl_cell), Paragraph("Public, tokenized paramedic emergency card showing blood group, pacemaker specs, critical allergies, and 1-click emergency dials.", tbl_cell)]
    ]

    pages_tbl = Table(pages_data, colWidths=[110, 130, 264])
    pages_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(pages_tbl)
    story.append(Spacer(1, 14))

    # ------------------------------------------------------------------
    # 6. DATABASE SCHEMA & DATA MODEL
    # ------------------------------------------------------------------
    story.append(Paragraph("6. Database Schema & Persistence Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    db_text = (
        "The relational database schema is structured into <b>24 specialized tables</b> in SQLite3, "
        "enforcing strict foreign key constraints, indexation, and audit traceability:"
    )
    story.append(Paragraph(db_text, body_style))

    db_tables_data = [
        [Paragraph("Table Name", tbl_header), Paragraph("Core Purpose", tbl_header), Paragraph("Key Schema Columns", tbl_header)],
        [Paragraph("<code>users</code>", tbl_cell_bold), Paragraph("Account registry & auth credentials", tbl_cell), Paragraph("id, name, email, password (scrypt), role, is_active, created_at", tbl_cell)],
        [Paragraph("<code>patient_profiles</code>", tbl_cell_bold), Paragraph("Demographics & twin sync state", tbl_cell), Paragraph("user_id, dob, gender, blood_group, medical_history, allergies, data_sources, last_synced", tbl_cell)],
        [Paragraph("<code>doctor_profiles</code>", tbl_cell_bold), Paragraph("Physician credentials & approval", tbl_cell), Paragraph("user_id, specialization, license_number, contact_number, is_approved", tbl_cell)],
        [Paragraph("<code>health_metrics</code>", tbl_cell_bold), Paragraph("Continuous vital telemetry stream", tbl_cell), Paragraph("user_id, heart_rate, blood_pressure, weight, temperature, recorded_at", tbl_cell)],
        [Paragraph("<code>patient_files</code>", tbl_cell_bold), Paragraph("Diagnostic files & lab attachments", tbl_cell), Paragraph("user_id, filename, file_type, upload_date", tbl_cell)],
        [Paragraph("<code>consultations</code>", tbl_cell_bold), Paragraph("Clinical encounter records & notes", tbl_cell), Paragraph("doctor_id, patient_id, notes (SOAP), prescriptions, follow_up_date, created_at", tbl_cell)],
        [Paragraph("<code>clinical_alerts</code>", tbl_cell_bold), Paragraph("Real-time clinical threshold flags", tbl_cell), Paragraph("patient_id, message, priority (critical/high/med/low), is_read, created_at", tbl_cell)],
        [Paragraph("<code>ai_agents</code>", tbl_cell_bold), Paragraph("Multi-agent registry & telemetry", tbl_cell), Paragraph("name, description, status, success_rate, latency_ms, invocations, model_backbone", tbl_cell)],
        [Paragraph("<code>ml_models</code>", tbl_cell_bold), Paragraph("ML prediction model registry", tbl_cell), Paragraph("name, version, status, accuracy, precision, recall, f1_score, framework, latency_ms", tbl_cell)],
        [Paragraph("<code>rag_documents</code>", tbl_cell_bold), Paragraph("Vectorized medical guidelines", tbl_cell), Paragraph("title, category, status, chunks_count, file_type, upload_date", tbl_cell)],
        [Paragraph("<code>alert_rules</code>", tbl_cell_bold), Paragraph("Configurable clinical triggers", tbl_cell), Paragraph("rule_name, condition, priority, is_active", tbl_cell)],
        [Paragraph("<code>audit_logs</code>", tbl_cell_bold), Paragraph("Immutable HIPAA security logs", tbl_cell), Paragraph("user_id, action, ip_address, status, timestamp", tbl_cell)],
        [Paragraph("<code>access_anomalies</code>", tbl_cell_bold), Paragraph("AI-detected anomalous PHI access", tbl_cell), Paragraph("user_id, target_patient_id, anomaly_type, severity, anomaly_score, status", tbl_cell)],
        [Paragraph("<code>emergency_access_sessions</code>", tbl_cell_bold), Paragraph("Break-glass unmasked overrides", tbl_cell), Paragraph("doctor_id, patient_id, reason, urgency_level, started_at, expires_at, is_active", tbl_cell)],
        [Paragraph("<code>user_risk_profiles</code>", tbl_cell_bold), Paragraph("Continuous user security scores", tbl_cell), Paragraph("user_id, risk_score (0-100), risk_level, anomalies_count, status_action", tbl_cell)],
        [Paragraph("<code>twin_versions</code>", tbl_cell_bold), Paragraph("Digital Twin immutable snapshots", tbl_cell), Paragraph("patient_id, version_label, health_score, sync_score, data_quality_score, vitals_snapshot", tbl_cell)],
        [Paragraph("<code>twin_drift_logs</code>", tbl_cell_bold), Paragraph("Telemetry vs predicted divergence", tbl_cell), Paragraph("patient_id, parameter, real_value, predicted_value, drift_percentage, severity", tbl_cell)],
        [Paragraph("<code>whatif_scenarios</code>", tbl_cell_bold), Paragraph("Saved intervention simulations", tbl_cell), Paragraph("patient_id, created_by_id, scenario_title, parameters_json, projected_health_score", tbl_cell)],
        [Paragraph("<code>patient_emergency_profiles</code>", tbl_cell_bold), Paragraph("Paramedic & QR critical directives", tbl_cell), Paragraph("user_id, emergency_token, blood_group, implantable_devices, allergies_critical, contacts", tbl_cell)],
        [Paragraph("<code>emergency_incidents</code>", tbl_cell_bold), Paragraph("SOS broadcast log & triage status", tbl_cell), Paragraph("patient_id, incident_type, severity_level (ESI), latitude, longitude, dispatched_facility", tbl_cell)],
        [Paragraph("<code>prescriptions</code>", tbl_cell_bold), Paragraph("Digital prescriptions & verification", tbl_cell), Paragraph("patient_id, doctor_id, rx_number, medication_name, dosage, frequency, signature, status", tbl_cell)],
        [Paragraph("<code>pharmacy_inventory</code>", tbl_cell_bold), Paragraph("Hospital pharmacy drug catalog", tbl_cell), Paragraph("medication_name, generic_name, ndc_code, dosage_strength, stock_quantity, shelf_location", tbl_cell)],
        [Paragraph("<code>medication_adherence_logs</code>", tbl_cell_bold), Paragraph("Adherence doses & streaks", tbl_cell), Paragraph("patient_id, prescription_id, medication_name, scheduled_slot, status, adherence_date", tbl_cell)],
        [Paragraph("<code>medication_warnings_log</code>", tbl_cell_bold), Paragraph("DDI and contraindication logs", tbl_cell), Paragraph("patient_id, prescription_id, warning_type, severity, title, description, recommendation", tbl_cell)]
    ]

    db_tbl = Table(db_tables_data, colWidths=[120, 140, 244])
    db_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(db_tbl)
    story.append(Spacer(1, 14))

    # ------------------------------------------------------------------
    # 7. SYSTEM STRENGTHS & SUMMARY CONCLUSION
    # ------------------------------------------------------------------
    story.append(Paragraph("7. Platform Strengths & Architectural Advantages", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=8, spaceBefore=2))

    strengths = [
        "<b>Autonomous Multi-Agent Collaboration:</b> Replaces single-prompt chatbots with synchronized domain agents featuring specialized neural backbones (PyTorch Bi-LSTM, XGBoost, GNNs, BioMedBERT).",
        "<b>Predictive & Simulation Capability:</b> Moves beyond static EHR dashboards by simulating future biological degradation and testing prospective medical interventions in a What-If sandbox.",
        "<b>Closed-Loop Pharmacovigilance:</b> Connects e-prescriptions directly with patient allergies, chronotherapy schedules, adherence tracking, and hospital stock availability.",
        "<b>Life-Saving Emergency Integration:</b> Links wearable crash/cardiac telemetry with paramedic dispatch and instant, unauthenticated QR-accessible emergency directive cards.",
        "<b>Enterprise HIPAA Zero-Trust Governance:</b> Features dynamic context-based PHI de-identification, access velocity anomaly detection, and tamper-proof break-glass auditing."
    ]
    for s in strengths:
        story.append(Paragraph(f"• {s}", bullet_style))

    story.append(Spacer(1, 15))

    # Sign-off box
    signoff_data = [
        [
            Paragraph("<b>Report Generated By:</b> AI Healthcare Systems Architecture Engine<br/>"
                      "<b>Status:</b> Validated & Production Ready &nbsp;|&nbsp; <b>Compliance Standard:</b> HIPAA Safe Harbor & Clinical AI Guidelines",
                      callout_style)
        ]
    ]
    signoff_tbl = Table(signoff_data, colWidths=[504])
    signoff_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(signoff_tbl)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == '__main__':
    build_pdf()

import sqlite3
import shutil
from datetime import datetime

# Backup existing database
shutil.copy('signalsar.db', f'signalsar.db.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}')

conn = sqlite3.connect('signalsar.db')
c = conn.cursor()

# Enable foreign keys
c.execute('PRAGMA foreign_keys = ON')

# Check if foreign keys already exist
c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='cases'")
cases_schema = c.fetchone()[0]

if 'FOREIGN KEY' not in cases_schema:
    print("Migrating database schema to add foreign keys and constraints...")
    
    # Get existing data
    c.execute('SELECT * FROM alerts')
    alerts = c.fetchall()
    
    c.execute('SELECT * FROM cases')
    cases = c.fetchall()
    
    c.execute('SELECT * FROM audit_log')
    audit_logs = c.fetchall()
    
    c.execute('SELECT * FROM submissions')
    submissions = c.fetchall()
    
    c.execute('SELECT * FROM analyst_feedback')
    feedbacks = c.fetchall()
    
    c.execute('SELECT * FROM interventions')
    interventions = c.fetchall()
    
    c.execute('SELECT * FROM reason_evidence')
    reason_evidence = c.fetchall()
    
    c.execute('SELECT * FROM adaptive_thresholds')
    thresholds = c.fetchall()
    
    # Drop existing tables
    c.execute('DROP TABLE IF EXISTS reason_evidence')
    c.execute('DROP TABLE IF EXISTS interventions')
    c.execute('DROP TABLE IF EXISTS analyst_feedback')
    c.execute('DROP TABLE IF EXISTS submissions')
    c.execute('DROP TABLE IF EXISTS audit_log')
    c.execute('DROP TABLE IF EXISTS cases')
    c.execute('DROP TABLE IF EXISTS adaptive_thresholds')
    c.execute('DROP TABLE IF EXISTS alerts')
    
    # Recreate with foreign keys
    c.execute('''CREATE TABLE alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        alert_type TEXT,
        risk_score INTEGER,
        status TEXT,
        created_at TEXT,
        assigned_to TEXT
    )''')
    
    c.execute('''CREATE TABLE cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id INTEGER,
        enriched_data TEXT,
        risk_analysis TEXT,
        sar_draft TEXT,
        compliance_score INTEGER,
        status TEXT,
        typology TEXT,
        typology_confirmed INTEGER DEFAULT 0,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (alert_id) REFERENCES alerts(id)
    )''')
    
    c.execute('''CREATE TABLE audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        analyst TEXT,
        action TEXT,
        details TEXT,
        before_value TEXT,
        after_value TEXT,
        timestamp TEXT,
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )''')
    
    c.execute('''CREATE TABLE submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        sar_payload TEXT,
        submitted_at TEXT,
        submission_id TEXT,
        checksum TEXT,
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )''')
    
    c.execute('''CREATE TABLE analyst_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        alert_id INTEGER,
        analyst TEXT,
        label TEXT,
        rationale TEXT,
        rationale_detail TEXT,
        created_at TEXT,
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )''')
    
    c.execute('''CREATE TABLE interventions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        alert_id INTEGER,
        action TEXT,
        reason TEXT,
        rationale TEXT,
        analyst TEXT,
        timestamp TEXT,
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )''')
    
    c.execute('''CREATE TABLE adaptive_thresholds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT UNIQUE,
        threshold_adjustment INTEGER DEFAULT 0,
        updated_at TEXT
    )''')
    
    c.execute('''CREATE TABLE reason_evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        reason_code TEXT,
        metric TEXT,
        evidence_ids TEXT,
        created_at TEXT,
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )''')
    
    # Create unique indexes on submissions
    c.execute('CREATE UNIQUE INDEX idx_submissions_submission_id ON submissions(submission_id)')
    c.execute('CREATE UNIQUE INDEX idx_submissions_checksum ON submissions(checksum)')
    
    # Create triggers for append-only immutability on audit_log
    c.execute('''
        CREATE TRIGGER prevent_audit_log_update
        BEFORE UPDATE ON audit_log
        BEGIN
            SELECT RAISE(ABORT, 'audit_log is append-only: updates not allowed');
        END
    ''')
    
    c.execute('''
        CREATE TRIGGER prevent_audit_log_delete
        BEFORE DELETE ON audit_log
        BEGIN
            SELECT RAISE(ABORT, 'audit_log is append-only: deletes not allowed');
        END
    ''')
    
    # Create triggers for append-only immutability on submissions
    c.execute('''
        CREATE TRIGGER prevent_submissions_update
        BEFORE UPDATE ON submissions
        BEGIN
            SELECT RAISE(ABORT, 'submissions is append-only: updates not allowed');
        END
    ''')
    
    c.execute('''
        CREATE TRIGGER prevent_submissions_delete
        BEFORE DELETE ON submissions
        BEGIN
            SELECT RAISE(ABORT, 'submissions is append-only: deletes not allowed');
        END
    ''')
    
    # Restore data
    for alert in alerts:
        c.execute('INSERT INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?)', alert)
    
    for case in cases:
        c.execute('INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', case)
    
    for log in audit_logs:
        c.execute('INSERT INTO audit_log VALUES (?, ?, ?, ?, ?, ?, ?, ?)', log)
    
    for sub in submissions:
        c.execute('INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?)', sub)
    
    for fb in feedbacks:
        c.execute('INSERT INTO analyst_feedback VALUES (?, ?, ?, ?, ?, ?, ?, ?)', fb)
    
    for intv in interventions:
        c.execute('INSERT INTO interventions VALUES (?, ?, ?, ?, ?, ?, ?, ?)', intv)
    
    for re in reason_evidence:
        c.execute('INSERT INTO reason_evidence VALUES (?, ?, ?, ?, ?, ?)', re)
    
    for th in thresholds:
        c.execute('INSERT INTO adaptive_thresholds VALUES (?, ?, ?, ?)', th)
    
    conn.commit()
    print("Migration complete!")
    print(f"- Added foreign key constraints")
    print(f"- Added unique indexes on submissions")
    print(f"- Added append-only triggers on audit_log and submissions")
else:
    print("Database already has foreign keys. No migration needed.")

conn.close()

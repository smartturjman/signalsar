import sqlite3
import json
from datetime import datetime, timedelta
import random

def init_db():
    conn = sqlite3.connect('signalsar.db')
    c = conn.cursor()
    
    # Enable foreign keys
    c.execute('PRAGMA foreign_keys = ON')
    
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        alert_type TEXT,
        risk_score INTEGER,
        status TEXT,
        created_at TEXT,
        assigned_to TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cases (
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
    
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log (
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
    
    c.execute('''CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        sar_payload TEXT,
        submitted_at TEXT,
        submission_id TEXT,
        checksum TEXT,
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS analyst_feedback (
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
    
    c.execute('''CREATE TABLE IF NOT EXISTS interventions (
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
    
    c.execute('''CREATE TABLE IF NOT EXISTS adaptive_thresholds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT UNIQUE,
        threshold_adjustment INTEGER DEFAULT 0,
        updated_at TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS reason_evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        reason_code TEXT,
        metric TEXT,
        evidence_ids TEXT,
        created_at TEXT,
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )''')
    
    # Create unique indexes on submissions
    c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_submissions_submission_id ON submissions(submission_id)')
    c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_submissions_checksum ON submissions(checksum)')
    
    # Create triggers for append-only immutability on audit_log
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_audit_log_update
        BEFORE UPDATE ON audit_log
        BEGIN
            SELECT RAISE(ABORT, 'audit_log is append-only: updates not allowed');
        END
    ''')
    
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_audit_log_delete
        BEFORE DELETE ON audit_log
        BEGIN
            SELECT RAISE(ABORT, 'audit_log is append-only: deletes not allowed');
        END
    ''')
    
    # Create triggers for append-only immutability on submissions
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_submissions_update
        BEFORE UPDATE ON submissions
        BEGIN
            SELECT RAISE(ABORT, 'submissions is append-only: updates not allowed');
        END
    ''')
    
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_submissions_delete
        BEFORE DELETE ON submissions
        BEGIN
            SELECT RAISE(ABORT, 'submissions is append-only: deletes not allowed');
        END
    ''')
    
    conn.commit()
    
    # Seed mock alerts
    c.execute('SELECT COUNT(*) FROM alerts')
    if c.fetchone()[0] == 0:
        mock_alerts = [
            ('CUST-8821', 'Rapid Movement', 94, 'open', (datetime.now() - timedelta(hours=2)).isoformat(), None),
            ('CUST-4455', 'NEW TYPOLOGY', 89, 'open', (datetime.now() - timedelta(hours=3)).isoformat(), None),
            ('CUST-5512', 'Structuring', 87, 'open', (datetime.now() - timedelta(hours=5)).isoformat(), None),
            ('CUST-3309', 'Network Link', 76, 'open', (datetime.now() - timedelta(hours=8)).isoformat(), None),
            ('CUST-7734', 'Velocity Spike', 68, 'open', (datetime.now() - timedelta(days=1)).isoformat(), None),
            ('CUST-2201', 'Unusual Pattern', 52, 'open', (datetime.now() - timedelta(days=2)).isoformat(), None),
        ]
        c.executemany('INSERT INTO alerts (customer_id, alert_type, risk_score, status, created_at, assigned_to) VALUES (?, ?, ?, ?, ?, ?)', mock_alerts)
        conn.commit()
    
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized")
